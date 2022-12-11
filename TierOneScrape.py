import re
import requests

from bs4 import BeautifulSoup

light_page = requests.get(str(input("What page would you like to scrape?")))
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
    get_request = session.get(new_url)
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
