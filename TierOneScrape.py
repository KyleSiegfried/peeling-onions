import re
import requests
import random
from bs4 import BeautifulSoup

ua_list = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19577"
    ,"Mozilla/5.0 (X11) AppleWebKit/62.41 (KHTML, like Gecko) Edge/17.10859 Safari/452.6", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2656.18 Safari/537.36"
    ,"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36", "Mozilla/5.0 (Linux; U; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13","Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"
    ,"Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"]
ua = random.choice(ua_list)
headers = {'User-Agent': ua}

light_page = requests.get(str(input("What page would you like to scrape?")), headers=headers)
content = BeautifulSoup(light_page.content, "html.parser")

def establish_tor_session():
    session = requests.session()
    session.proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    return session

session = establish_tor_session

def peel(new_url, company):
    get_request = session.get(new_url, headers=headers)
    parsed_dark_page = BeautifulSoup(get_request.text, 'html.parser')
    raw_text = parsed_dark_page.get_text()
    return company in raw_text      

def filter_onions(company):
    onions = []
    for a in content.find_all('a', href=True):
        if re.match(r"([^\s]+\.)(onion|pet)$", a['href']) is not None:
            onions.append(re.sub(r"(\.([^\s]+))$", ".onion", a['href']))
    for new_url in onions:
        print(new_url + ": " + str(peel(new_url, company)))

filter_onions(str(input("What company would you like to query for? ")))
