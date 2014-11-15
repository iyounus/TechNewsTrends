from bs4 import BeautifulSoup
import requests
import json
import time
from dateutil import parser

import re

from pymongo import MongoClient
from pymongo import errors

'''
This code is adopted from Jonathan's solution to web-scraping exercise.
This downloads articles from NYT be using urls saved in mongodb.
'''


client = MongoClient()
db = client.nyt_tech

# get mongoDB collection
collection = db.articles


for article in collection.find({'html' : {'$exists' : False} }):
    if not article.has_key('html') and article['document_type'] == 'article':
        date  = parser.parse(article['pub_date'])
        start = parser.parse("2015-01-01T00:00:00Z")
        end   = parser.parse("2011-01-01T00:00:00Z")
        if date > start or date < end:
            continue

        if '/reuters/' in article['web_url']:
            continue

        if '/aponline/' in article['web_url']:
            continue
           
        #print article['web_url']
        # time.sleep(1)
        html = requests.get(article['web_url'] + "?smid=tw-nytimes")

        if html.status_code == 200:
            soup = BeautifulSoup(html.text, "html.parser")
            # serialize html
            
            # this works for 2014 articles only

            txt = [p.text for p in soup.findAll('p', class_='story-body-text story-content')]

            # this works for articles before 2014
            if len(txt) == 0:
                txt = [p.text for p in soup.findAll('p', {"itemprop" : "articleBody"})]

            if len(txt) == 0:
                txt = [p.text for p in soup.findAll('div', {"class" : "articleBody"})]

            if len(txt) == 0:
                txt = [p.text for p in soup.findAll('div', {"id" : "articleBody"})]

            if len(txt)>0:
                txt = " ".join(txt)
                txt = re.sub('[^\w\s]+', ' ', txt).replace('\n',' ')

                print article['web_url']

                collection.update({ '_id' : article['_id'] }, { '$set' : { 'html' : unicode(soup) } } )
                collection.update({ '_id' : article['_id'] }, { '$set' : { 'content' : txt } })
            else:
                print "NO TEXT FOUND ", article['web_url']
