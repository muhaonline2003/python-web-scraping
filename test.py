import requests
import json

import sys
sys.path.insert(0,'bs4.zip')
from bs4 import BeautifulSoup

# Imitate the Mozilla browser.
user_agent = {'User-agent':'Mozilla/5.0'}

def compare_prices(product_laughs, product_glomark):
    # TODO: Acquire the web pages that contain product prices.
    laughs_req = requests.get(product_laughs, headers=user_agent)
    laughs_soup = BeautifulSoup(laughs_req.content, 'html.parser')

    glomark_req = requests.get(product_glomark, headers=user_agent)
    glomark_soup = BeautifulSoup(glomark_req.content, 'html.parser')

    product_name_laughs_elem = laughs_soup.find("div", {"class":"product-name"})
    if product_name_laughs_elem is not None:
        product_name_laughs = product_name_laughs_elem.text.strip()
    else:
        product_name_laughs = "Product name not found"

    product_name_glomark_elem = glomark_soup.find("div", {"class":"product-title"})
    if product_name_glomark_elem is not None:
        product_name_glomark = product_name_glomark_elem.text.strip()
    else:
        product_name_glomark = "Product name not found"

    # TODO: LaughsSuper supermarket website provides the price in a span text.
    price_laughs = float(laughs_soup.find("span", {"class":"regular-price"}).text.strip()[3:].replace(',', ''))

    # TODO: Glomark supermarket website provides the data in json format in an inline script.
    # You can use the json module to extract only the price
    price_glomark = float(json.loads(glomark_soup.find("script", {"type": "application/ld+json"}).text.strip())['offers'][0]['price'])

    # TODO: Parse the values as floats, and print them.
    print('Laughs  ', product_name_laughs, 'Rs.: ', price_laughs)
    print('Glomark ', product_name_glomark, 'Rs.: ', price_glomark)

    if price_laughs > price_glomark:
        print('Glomark is cheaper Rs.:', price_laughs - price_glomark)
    elif price_laughs < price_glomark:
        print('Laughs is cheaper Rs.:', price_glomark - price_laughs)
    else:
        print('Price is the same')
