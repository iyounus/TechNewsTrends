import numpy as np
import pandas as pd
import pickle as pkl
import os
import sys

import matplotlib.pyplot as plt
from wordcloud import WordCloud

#from write_web_app_csv import assign_topics
from utils import stop_words, tokenize


def draw_word_cloud(df, topic, n_articles=50, save=True):
    ftopic = df[df['topic_sorted']==topic]
    ftopic = ftopic.sort('weight', ascending=False).head(n_articles)

    text = list(ftopic['content'].values)
    text = " ".join(text)
    #remove stop words and lemmatize
    text = tokenize(text) # but this tokenizes again!
    text = " ".join(text)

    wordcloud = WordCloud().generate(text)
    plt.figure(figsize=(6,4))
    plt.imshow(wordcloud)
    plt.axis("off")

    if save:
        fileName = outdir + "topic_"+str(topic)+"temp.png"
        plt.savefig(fileName, bbox_inches='tight')


def assign_topics(df, modle, vectors):
    W = model.components_
    A = vectors.dot(W.T)

    df['topic'] = list(np.argmax(A, axis=1))
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


if __name__=="__main__":
    s_topics = sys.argv[1] # this is a string
    n_topics = int(s_topics)

    outdir = 'topic_browser/static/'

    df = pkl.load(open('data/data_all.pkl'))
    model = pkl.load(open('data/model_' + str(n_topics) + '.pkl'))
    vectorizer, vectors = pkl.load(open('data/vectorizer.pkl', "rb"))

    df = assign_topics(df, model, vectors)

    for i in range(n_topics):
        draw_word_cloud(df, i)

    # trim output wordcloud images using imagemagick convert function
    for i in range(n_topics):
        fileName = outdir + 'topic_' + str(i) + 'temp.png'
        os.system('convert ' + fileName + ' -trim ' + \
                  outdir + 'topic_' + s_topics + '_' + str(i) + '.png')
        os.system('rm ' + fileName)
