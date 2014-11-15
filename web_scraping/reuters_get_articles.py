from bs4 import BeautifulSoup
import requests

import time
import random

import re

from pymongo import MongoClient
from pymongo import errors


def init_mongo():
    client = MongoClient()
    db = client.reuters
    collection = db.articles
    return db, collection


if __name__ == '__main__':
    db, collection = init_mongo()

    with open("reuters_urls_unique_2012.txt") as f:
        urls = f.read().splitlines()

    print "total urls: ", len(urls)

    for url in urls:
        if collection.find_one({'web_url' : url}):
            print 'duplicate'
            continue

        time.sleep(random.uniform(0,2)) # just in case

        html = requests.get(url)

        d = {}
        if (html.status_code) == 200:
            soup = BeautifulSoup(html.text, "html.parser")
            head = soup.find("h1").text
            pub_date = soup.find("span", {"class":"timestamp"}).text
            txt = soup.find("span", {"id":"articleText"}).text
            txt = re.sub('[^\w\s]+', ' ', txt).replace('\n',' ')
            d['web_url'] = url
            d['content'] = txt
            d['headline'] = head
            d['pub_date'] = pub_date
            print url
            collection.insert(d)
