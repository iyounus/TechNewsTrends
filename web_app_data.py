from __future__ import division

import numpy as np
import pandas as pd
import pickle as pkl
import unicodedata
import sys

from datetime import date, timedelta as tdel

class WebAppData(object):

    def __init__(self, df, model, vectors):
        self.df = df
        self.nmf = model
        self.vectors = vectors

        self.data = [] # data to be writtne in csv file

        self.add_features()
        self.assign_topics()


    def add_features(self):
        '''
        Adds new columns to DataFrame which are need for csv file output.
        '''
        # add columns needed for analysis
        self.df['pub_date'] = pd.to_datetime(self.df['pub_date'])
        self.df['pub_week'] = self.df.pub_date.map(lambda x: date.isocalendar(x)[1])
        self.df['pub_year'] = self.df.pub_date.map(lambda x: date.isocalendar(x)[0])
        self.df['pub_month'] = self.df.pub_date.map(lambda x: x.month)
        self.df['pub_week_date'] = \
            self.df.pub_date.map(lambda x : x.date() + tdel(0-x.date().weekday()))
                                                     # 0 -> Monday of the pub_week
        self.df['pub_week_date_str'] = \
            self.df.pub_date.map(lambda x : (x.date() + tdel(0-x.date().weekday()))
                                            .strftime("%Y-%m-%d"))

    def assign_topics(self):

        W = self.nmf.components_
        A = self.vectors.dot(W.T)

        self.df['topic'] = list(np.argmax(A, axis=1))
        self.df['weight'] = list(np.max(A, axis=1))
        self.df = self.df[self.df['weight']>0.5]

        # now sort topics w.r.t number of articles per topic
        # this is just renaming the topic
        dg = self.df[['topic','headline']].groupby('topic')
        x = sorted(dg.groups.keys())
        y = [len(dg.groups[i]) for i in x]
        m = list(np.argsort(y)[::-1])
        d = {j : x[i] for i, j in enumerate(m)}

        self.df['topic_sorted'] = self.df['topic'].map(lambda x : d[x])


    def articles_week_dict(self): #articles per week
        dg = self.df[['pub_week_date_str','headline']].groupby('pub_week_date_str')
        return dg.size().to_dict()


    def articles_week(self, outfile):
        d = self.articles_week_dict()
        f = open(outfile,'w')
        f.write("date,articles_week\n")

        keylist = sorted(d.keys())
        for key in keylist:
            f.write(key+','+str(d[key])+'\n')
        f.close()


    def articles_topic(self, outfile): #articles per topic
        dg = self.df[['topic_sorted','headline']].groupby('topic_sorted')
        x = sorted(dg.groups.keys())
        y = [len(dg.groups[i]) for i in x]

        f = open(outfile,'w')
        f.write("ntopic,frequency\n")
        for i,val in enumerate(x):
            f.write(str(val)+','+str(y[i])+'\n')
        f.close()


    def articles_topic_week(self, outfile): #articles per topic per week
        '''
        INPUT DataFrame
        OUTPUT DataFrame

        creats DataFrame to be written to csv file which is used by web app
        '''
        #columns to be written in csv file
        col0 = ['topic_sorted','pub_week','pub_week_date','headline','web_url']
        col1 = ["headline"+str(i) for i in range(5)]
        col2 = ['url'+str(i) for i in range(5)]

        d = self.articles_week_dict()
        for topic in self.df['topic_sorted'].order().unique().tolist():
            for pub_week_date in self.df['pub_week_date'].order().unique().tolist():
                pub_week_date_str = pub_week_date.strftime("%Y-%m-%d")

                cond = "topic_sorted == " + str(topic) + \
                       " & pub_week_date_str == '" + pub_week_date_str + "'"
                dg = self.df.query(cond).sort(['weight'], ascending=[0])[col0]

                headlines = [unicodedata.normalize('NFKD', h).encode('ascii','ignore')
                             for h in dg['headline'].values.tolist()]
                urls = dg['web_url'].values.tolist()

                row = {}
                #if (len(urls) > 0):
                row['n_articles'] = len(urls)
                row['fraction'] = len(urls)/d[pub_week_date_str]
                row['pub_week_date'] = pub_week_date_str
                row['topic'] = topic
                row['pub_week'] = date.isocalendar(pub_week_date)[1]
                for i in range(len(col1)):
                    if i < len(urls):
                        row[col2[i]] = urls[i]
                        row[col1[i]] = headlines[i]
                    else:
                        row[col2[i]] = "x" # just a place holder
                        row[col1[i]] = "x"

                self.data.append(row)

        newdf = pd.DataFrame(self.data)
        # rearrange columns
        newdf = newdf[['topic','pub_week','n_articles','fraction','pub_week_date']+
                        col1+col2]
        newdf.to_csv(outfile, index=False)


    def wrtie_data(self, outfile1, outfile2, outfile3):
        self.articles_topic(outfile1)
        self.articles_week(outfile2)
        self.articles_topic_week(outfile3)


if __name__=='__main__':
    n_topics = int(sys.argv[1])

    df = pkl.load(open('data/data_all.pkl'))
    model = pkl.load(open('data/model_'+str(n_topics)+'.pkl'))
    vectorizer, vectors = pkl.load(open('data/vectorizer.pkl', "rb"))

    app_data = WebAppData(df, model, vectors)

    app_data.wrtie_data('topic_browser/static/articles_per_topic.csv',
                        'topic_browser/static/articles_per_week.csv',
                        'topic_browser/static/data.csv')

