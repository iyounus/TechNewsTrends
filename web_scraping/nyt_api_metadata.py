import requests
import json
import time

from dateutil import parser
from pymongo import MongoClient
from pymongo import errors


def init_mongo():
    # SETUP MONGO DB CONNECTION VIA PYMONGO
    client = MongoClient()

    # CREATE DATABASE NAMED nyt_tech
    db = client.nyt_tech

    # CREATE A COLLECTION IN NYT NAMED articles (SHORTCUT TO NAMED COLLECTION)
    collection = db.articles
    return db, collection


def GetLatestEntryDate():
    '''
    INPUT None
    OUTPUT date
    
    This function takes a mongo db collection as input and returns the 
    date of the last entry in the db
    '''

    entry = collection.find().sort('pub_date').limit(1).next()
    return parser.parse(entry['pub_date']).strftime("%Y%m%d")


# This code is copied from the Jonathan's solution for web_scraping exercise
def scraper():
    '''
    INPUT  None
    OUTPUT None

    Gets metadata for NYT articles using NYT api
    '''

    max_pages = 10000
    page = 0
    final_page = 0
    page_count = 0
    cursor_count = 0
    articles_left = total_articles
    latest_article = ""

    last_date = ""
    if not collection.find_one():
        last_date = "20141103"
    else:
        last_date = GetLatestEntryDate()


    # let us loop (and hopefully not hit our rate limit)
    while articles_left > 0 and page_count < max_pages:
        if  articles_left%100==0:
            print "Articles left: ", articles_left

        url = api_url + "&page=" + str(page) + "&end_date=" + str(last_date)
        more_articles = requests.get(url)
        # make sure it was successful
        if more_articles.status_code == 200:
            for content in more_articles.json()['response']['docs']:
                #print content['web_url']
                latest_article = parser.parse(content['pub_date'])\
                    .strftime("%Y%m%d")

                if not collection.find_one(content):
                    try:
                        collection.insert(content)
                    except errors.DuplicateKeyError:
                        print "Duplicates"
                        continue
                else:
                    print "In collection already"
                    
            articles_left -= 10

            page += 1
            page_count += 1
            cursor_count += 1
            final_page = max(final_page, page)
        else:
            if more_articles.status_code == 403:
                print "Sleepy..."
                # account for rate limiting
                time.sleep(2)
            elif cursor_count > 100:
                print "Adjusting date"
                cursor_count = 0
                page = 0
                last_date = latest_article
            else:
                print "ERRORS: " + str(more_articles.status_code)
                cursor_count = 0
                page = 0
                last_date = latest_article


if __name__ == '__main__':
    api_key = '4ab21f2ea4bb6a0893135fbf0881689d:15:69947362'
    api_url = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?sort=newest&fq=section_name:"Technology"&api-key=' + api_key

    db, collection = init_mongo()
    
    api = requests.get(api_url)
    total_articles = articles_left = api.json()['response']['meta']['hits']

    scraper()


