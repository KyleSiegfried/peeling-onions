import requests
from bs4 import BeautifulSoup

url = "https://darkfeed.io/ransomgroups/"

page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
for a in soup.find_all('a', href=True):
    if "darkfeed.io" not in a['href'] and "twitter.com" not in a['href'] and "t.me" not in a['href'] and "javascript:void(0);" not in a['href'] and "#" not in a['href']:
        print(a['href'])