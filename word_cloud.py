import numpy as np
import pandas as pd
import pickle as pkl
import os
import sys

import matplotlib.pyplot as plt
from wordcloud import WordCloud

from write_web_app_csv import assign_topics
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


if __name__=="__main__":
    n_topics = int(sys.argv[1])

    outdir = "topic_browser/static/"
    modle_file = 'data/model_' + str(n_topics) + '.pkl'

    df = pkl.load(open("data/data_all.pkl"))
    df = assign_topics(df, modle_file=modle_file,
                           vector_file='data/vectorizer.pkl')

    for i in range(n_topics):
        draw_word_cloud(df, i)

    # trim output wordcloud images using imagemagick convert function
    for i in range(n_topics):
        fileName = outdir + "topic_" + str(i) + "temp.png"
        os.system("convert " + fileName + " -trim " + \
                  outdir + "topic_" + str(i) + ".png")
        os.system("rm " + fileName)
