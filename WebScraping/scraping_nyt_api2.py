# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

NYT_URL = 'http://api.nytimes.com/svc/search/v2/articlesearch.json'
API_KEY = "4ab21f2ea4bb6a0893135fbf0881689d:15:69947362"

# <codecell>

from bs4 import BeautifulSoup
import requests
import json
import time
from dateutil import parser
from pymongo import MongoClient
from pymongo import errors

# <codecell>

def init_mongo():
    # SETUP MONGO DB CONNECTION VIA PYMONGO
    client = MongoClient()

    # CREATE DATABASE NAMED NYT
    db = client.nyt

    # CREATE A COLLECTION IN NYT NAMED ARTICLES (SHORTCUT TO OT NAMED COLLECTION)
    collection = db.articles
    return db, collection

# <codecell>

payload  = {'sort': 'newest', 'begin_date': '20140901', 'end_date': '20141001',
                'api-key': API_KEY, 
                'page': 0}

api = requests.get(NYT_URL, params=payload)
print dir(api)

# <codecell>

#r = api.json()['response']
api.ok

# <codecell>

db, collection = init_mongo()
collection.insert(r)

# <codecell>

collection.remove()

# <codecell>

for doc in r['docs']:
    collection.insert(doc)

# <codecell>

for i in xrange(1,10):
    payload  = {'sort': 'newest',
                'begin_date'='20140901',
                'end_date'='20141001',
                'api-key': API_KEY, 
                'page': i}

    api = requests.get(NYT_URL, params=payload)
    r = api.json()['response']
    
    for doc in r['docs']:
        collection.insert(doc)

# <codecell>

#days = 2
d = datetime.date(2014,9,30)
days = 31
while days < 60:
    datestr = (d - datetime.timedelta(days=days)).strftime('%Y%m%d')
    page = 0
    payload  = {'sort': 'newest', 'begin_date': datestr, 'end_date': datestr,
                    'api-key': API_KEY, 
                    'page': page}
    api = requests.get(NYT_URL, params=payload)
    while api.ok:
        r = api.json()['response']
        for doc in r['docs']:
            try:
              collection.insert(doc)
            except:
               print 'skipped one'
        page += 1
        print 'page:' , page
        payload  = {'sort': 'newest', 'begin_date': datestr, 'end_date': datestr,
                    'api-key': API_KEY, 
                    'page': page}
        time.sleep(.1)
        api = requests.get(NYT_URL, params=payload)
    print 'done'
    days += 1

# <codecell>

print days
print page

# <codecell>

import datetime
d = datetime.date(2014,9,30)

# <codecell>

days = 1
(d - datetime.timedelta(days=days)).strftime('%Y%m%d')

# <codecell>

for doc in r['docs']:
        try:
            collection.insert(doc)
        except:
            print 'skipped one'
              

# <codecell>


