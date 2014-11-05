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

limit = 35000

for article in collection.find({'html' : {'$exists' : False} }):
    if limit and limit > 0:
        if not article.has_key('html') and article['document_type'] == 'article':
            limit -= 1

            if not '2013' in article['pub_date']:
                continue

            time.sleep(1)
            html = requests.get(article['web_url'] + "?smid=tw-nytimes")

            if html.status_code == 200:
                soup = BeautifulSoup(html.text, "html.parser")
                # serialize html
                
                # this works for 2014 articles only
                #txt = [p.text for p in soup.findAll('p', class_='story-body-text story-content')]

                # this works for articles before 2014
                txt = [p.text for p in soup.findAll('p', {"itemprop" : "articleBody"})]

                if len(txt)>0:
                    txt = " ".join(txt)
                    txt = re.sub('[^\w\s]+', ' ', txt).replace('\n',' ')

                    print article['web_url']

                    collection.update({ '_id' : article['_id'] }, { '$set' : { 'html' : unicode(soup) } } )
                    collection.update({ '_id' : article['_id'] }, { '$set' : { 'content' : txt } })
                else:
                    print "NO TEXT FOUND ", article['web_url']
