from bs4 import BeautifulSoup
import requests
import json
import time
from dateutil import parser

from pymongo import MongoClient
from pymongo import errors

'''
This copied from Jonathan's solution to web-scraping exercise. This downloads
articles from NYT be using urls saved in mongodb.
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
            print article['web_url']
            html = requests.get(article['web_url'] + "?smid=tw-nytimes")
            
            if html.status_code == 200:
                soup = BeautifulSoup(html.text)

                # serialize html
                collection.update({ '_id' : article['_id'] }, { '$set' : { 'html' : unicode(soup), 'content' : [] } } )
            
                for p in soup.find_all('div', class_='articleBody'):
                    collection.update({ '_id' : article['_id'] }, { '$push' : { 'content' : p.get_text() } })
