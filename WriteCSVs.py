import numpy as np
import pandas as pd
import pickle as pkl
import unicodedata

from datetime import date, timedelta as tdel

def creat_df(pickle_file):
    '''
    INPUT string
    OUTPUT DataFrame

    Reads DataFrame from pickle file created by MongoToDataFrame, and 
    adds new columns to DataFrame which are need for csv file output.
    '''
    df = pkl.load(open(pickle_file))

    # add columns needed for analysis
    df['pub_date'] = pd.to_datetime(df['pub_date'])
    df['pub_week'] = df.pub_date.map(lambda x : date.isocalendar(x)[1])
    df['pub_year'] = df.pub_date.map(lambda x : date.isocalendar(x)[0])
    df['pub_month'] = df.pub_date.map(lambda x : x.month)
    df['pub_week_date'] = df.pub_date.map(lambda x : x.date() + 
                                          tdel(0-x.date().weekday()))
                                          # 0 -> Monday of the pub_week
    df['pub_week_date_str'] = \
        df.pub_date.map(lambda x : (x.date() + tdel(0-x.date().weekday()))
                                    .strftime("%Y-%m-%d"))
    return df


def assign_topics(df, modle_file, vector_file):
    vectors = pkl.load(open(vector_file, "rb"))
    nmf = pkl.load(open(modle_file, "rb"))

    W = nmf.components_
    A = vectors.dot(W.T)

    df['topic'] = list(np.argmax(A, axis=1)) # topic number starts from 0
    df['weight'] = list(np.max(A, axis=1))

    # now sort topics w.r.t number of articles per topic
    # this is just renaming the topic
    dg = df[['topic','headline']].groupby('topic')
    x = sorted(dg.groups.keys())
    y = [len(dg.groups[i]) for i in x]
    m = list(np.argsort(y)[::-1])
    d = {j : x[i] for i, j in enumerate(m)}

    df['topic_sorted'] = df['topic'].map(lambda x : d[x])

    return df


def articles_per_topic(df, outfile):
    dg = df[['topic_sorted','headline']].groupby('topic_sorted')
    x = sorted(dg.groups.keys())
    y = [len(dg.groups[i]) for i in x]

    f = open(outfile,'w')
    f.write("ntopic,frequency\n")
    for i,val in enumerate(x):
        f.write(str(val)+','+str(y[i])+'\n')
    f.close()


def creat_data_csv(df):
    '''
    INPUT DataFrame
    OUTPUT DataFrame

    creats DataFrame to be written to csv file which is used by web app
    '''
    #columns to be written in csv file
    col0 = ['topic_sorted','pub_week','pub_week_date','headline','web_url']
    col1 = ["headline"+str(i) for i in range(5)]
    col2 = ['url'+str(i) for i in range(5)]

    j = []
    for topic in df['topic_sorted'].order().unique().tolist():
        for pub_week_date in df['pub_week_date'].order().unique().tolist():
            pub_week_date_str = pub_week_date.strftime("%Y-%m-%d")

            cond = "topic_sorted == " + str(topic) + \
                   " & pub_week_date_str == '" + pub_week_date_str + "'"
            dg = df.query(cond).sort(['weight'], ascending=[0])[col0]

            headlines = [unicodedata.normalize('NFKD', h).encode('ascii','ignore')
                         for h in dg['headline'].values.tolist()]
            urls = dg['web_url'].values.tolist()

            row = {}
            #if (len(urls) > 0):
            row['N_articles'] = len(urls)
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

            j.append(row)

    return pd.DataFrame(j)


if __name__=='__main__':
    df = creat_df('data/data_all.pkl')
    df = assign_topics(df, modle_file='data/model_30.pkl',
                           vector_file='data/vector.pkl')

    articles_per_topic(df, "TopicBrowser/static/articles_per_topic.csv")
    newdf = creat_data_csv(df)
    newdf.to_csv("TopicBrowser/static/data.csv", index=False)
