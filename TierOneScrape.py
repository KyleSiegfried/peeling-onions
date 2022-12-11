from bs4 import BeautifulSoup
import random
import re
import requests

#Company we are scraping for
company = str(input("What company do you want to scrape for? "))

#List of spoofed user agents to prevent site from blocking our traffic
ua_list = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19577"
    ,"Mozilla/5.0 (X11) AppleWebKit/62.41 (KHTML, like Gecko) Edge/17.10859 Safari/452.6", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2656.18 Safari/537.36"
    ,"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36", "Mozilla/5.0 (Linux; U; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13","Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"
    ,"Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"]
ua = random.choice(ua_list)
headers = {'User-Agent': ua}

#Scrapes HTML from light web page and spoofs our user agent in the header of the get-request
light_page = requests.get("https://darkfeed.io/ransomgroups/", headers=headers)
#light_page = requests.get(str(input("What page would you like to scrape? ")), headers=headers)

#Parses HTML from the get-request above
content = BeautifulSoup(light_page.content, "html.parser")

#Array of compiled links to check
to_scrape = []

#.onion links we have already scraped
checked_onions = []

#Routes our traffic through the default Tor port running on our host OS
def establish_tor_session():
    session = requests.session()
    session.proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    return session

#Sets our session to the Tor session
session = establish_tor_session()

def peel_sub(main_onion, main_number):
    """A function to find more urls."""
    try:
        horizontal_dark_page = session.get(main_onion, headers=headers)
        if horizontal_dark_page.status_code == int(200):
            to_scrape.append(main_onion)
            hdp_content = BeautifulSoup(horizontal_dark_page.text, 'html.parser')
            second_number = int(1)
            for a2 in hdp_content.find_all('a', href=True):
                hdp_links = a2['href']
                if main_onion in hdp_links and hdp_links not in checked_onions and hdp_links not in to_scrape:
                    #peel_second(hdp_links, main_onion, company)
                    to_scrape.append(hdp_links)
                    
                    print(str(main_number) + "." + str(second_number) + " Appending Secondary")
                    second_number = second_number+1
    except:
        print("Session Error")

#Filters for <a> tags containing .onion top-level domain from light web HTML get-request
def filter_onions():
    main_number = int(1)
    for a in content.find_all('a', href=True):
        if re.match(r"([^\s]+\.)(onion|pet)$", a['href']) is not None:
            #Replaces top-level domain with .onion
            main_onion = re.sub(r"(\.([^\s]+))$", ".onion", a['href'])
            print(str(main_number) + " Appending Main")
            peel_sub(main_onion, main_number)
            main_number = main_number+1                

filter_onions()

#Scrapes to_scrape links for text containing the company name provided by user input
def scraper(company):
    for url in to_scrape:
        dark_page = session.get(url, headers=headers)
        dark_content = BeautifulSoup(dark_page.text, 'html.parser')
        raw_text = dark_content.get_text()
        checked_onions.append(url)
        if company in raw_text.lower():
            print(url + ": " + "Compromised")
scraper(company.lower())
    
