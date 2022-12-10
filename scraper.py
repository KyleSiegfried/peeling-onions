import requests

from bs4 import BeautifulSoup

page = requests.get("https://darkfeed.io/ransomgroups/")
soup = BeautifulSoup(page.content, "html.parser")
checked = []

def peel(onion, phrase):
    """A function to check for phrase"""
    html_2 = requests.get(onion)
    soup_3 = BeautifulSoup(html_2, 'html.parser')
    raw_text = soup_3.get_text()
    return phrase in raw_text

def scrape(onion, main_onion, phrase):
    """A function to find more urls."""
    html = requests.get(onion)
    soup_2 = BeautifulSoup(html, 'html.parser')

    hits = []

    for a_2 in soup_2.find_all('a', href=True):
        if main_onion in a_2['href'] and a_2['href'] not in checked:
            hits = hits + scrape(a_2['href'], main_onion, phrase)
    
    if peel(onion, phrase):
        hits.append(onion)

    checked.append(onion)
    return hits

def check_for_bad_onion(phrase):
    """A function to check if an onion is bad"""
    to_check = []

    for a in soup.find_all('a', href=True):
        if "darkfeed.io" not in a['href'] and "twitter.com" not in a['href'] and "t.me" not in a['href'] and "javascript:void(0);" not in a['href'] and "#" not in a['href']:
            to_check.append(a['href'])

    for check in to_check:
        print(check + ": " + len(scrape(check, check, phrase)))
        checked.append(to_check.pop())

check_for_bad_onion(str(input("What company would you like to search for?")))