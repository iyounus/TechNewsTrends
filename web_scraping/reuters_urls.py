
from bs4 import BeautifulSoup
import json
import requests
import random

import time
from pymongo import MongoClient
from pymongo import errors
import re

def init_db():
    client = MongoClient()
    db = client.nyt_tech
    # get mongoDB collection
    collection = db.articles
    return collection


def gen_urls():
    s = lambda x : str(x) if x > 9 else '0'+str(x)
    for month in range(1,13):
        for day in range(1,32):
            date = '2012'+s(month)+s(day)
            url = 'http://www.reuters.com/resources/archive/us/'+date+'.html'
            yield url


def get_html(url):
    print url
    time.sleep(random.uniform(0,2)) # just in case

    html = requests.get(url)
    l = []
    if (html.status_code) == 200:
        soup = BeautifulSoup(html.text, "html.parser")
        l = [(href.find('a').text, href.find('a').get('href')) \
            for href in soup.findAll('div', class_='headlineMed')]
    return l


if __name__=='__main__':
    mongo = init_db()

    with open("nyt_2012_headlines.txt") as f:
        headlines = f.read().lower().splitlines()

    print type(headlines[0])

    output = []

    for url in gen_urls():
        l = get_html(url)
        print len(l), 'urls found on reuters'

        for headline, url in l:
            s_headline = ""
            try:
                s_headline = str(headline).lower()
            except UnicodeEncodeError:
                pass

            if s_headline in headlines:
                print "getTHIS ", url, ",", s_headline
                output.append((url, s_headline))

    f = open('reuters_urls_2012.txt','w')
    for url,headline in output:
        headline = re.sub('[^\w\s]+', ' ', headline)
        f.write(url+','+headline+'\n')
    f.close()
