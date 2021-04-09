import requests
import lxml
from bs4 import BeautifulSoup

def get_link_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36",
        "Accept-Language": "en",
    }

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    name = soup.select_one(selector="#productTitle").getText()
    name = name.strip()

    price = soup.select_one(selector="#priceblock_ourprice").getText()
    price = price.replace(',', '')
    price = float(price[1:])

    return name, price