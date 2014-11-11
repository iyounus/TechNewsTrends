import numpy as np
import pandas as pd
import pickle as pkl
import os

from wordcloud import WordCloud
from WriteCSVs import assign_topics
from utils import stop_words, tokenize

import matplotlib.pyplot as plt


def DrawWordCloud(df, topic, n_articles=50, save=True):
    ftopic = df[df['topic']==topic].sort('weight',ascending=False).head(n_articles)
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
        fileName = "topic_"+str(topic+1)+"temp.png"
        plt.savefig(fileName, bbox_inches='tight')


if __name__=="__main__":
    df = pkl.load(open("nyt_tech_temp.pkl"))
    df = assign_topics(df, modle_file='model.pkl', vector_file='vectors.pkl')

    n_topics = 10
    for i in range(n_topics):
        DrawWordCloud(df, i)

    # trim output wordcloud images using imagemagick convert function
    for i in range(n_topics):
        fileName = "topic_" + str(i+1) + "temp.png"
        os.system("convert " + fileName + " -trim " + \
                  "topic_" + str(i+1) + ".png")
        os.system("rm " + fileName)
