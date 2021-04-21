import requests
import lxml
from bs4 import BeautifulSoup
from textblob import TextBlob
import pandas as pd

def get_link_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36",
        "Accept-Language": "en",
    }

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    name = soup.select_one(selector="#productTitle").getText()
    name = name.strip()

    try:
        price = soup.select_one(selector="#priceblock_ourprice").getText()
    except AttributeError:
        try:
            price = soup.select_one(selector="#priceblock_saleprice").getText()
        except AttributeError:
            try:
                price = soup.select_one(selector="#priceblock_dealprice").getText()
            except:
                return name, 0

    price = price.replace(',', '')
    price = float(price[1:])

    try:
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip()
        except:
            rating = ""

    review = soup.findAll('div',class_="a-expander-content reviewText review-text-content a-expander-partial-collapse-content")

    review_list = []
    top_reviews = pd.DataFrame()
    pol = lambda x: TextBlob(x).sentiment.polarity
    sub = lambda x: TextBlob(x).sentiment.subjectivity

    for re in review:
        review_list.append(re.span.text.replace("\n", ""))

    def getAnalysis(score):
        if score < 0:
            return 'Negative'
        elif score == 0:
            return 'Neutral'
        else:
            return 'Positive'

    top_reviews['Review']=review_list
    top_reviews['Polarity'] = top_reviews['Review'].apply(pol)
    top_reviews['Subjectivity'] = top_reviews['Review'].apply(sub)
    top_reviews['Analysis'] = top_reviews['Polarity'].apply(getAnalysis)

    return name, price, rating, top_reviews