import pandas as pd
import pickle as pkl
import sys

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

from utils import stop_words, tokenize

class Model(object):

    def __init__(self, n_topics, n_features=5000, df=None,
                 vectorizer=None, vector=None, outdir='data/'):
        self.n_topics = n_topics
        self.n_features = n_features
        self.df = df
        self.vectorizer = vectorizer
        self.vector = vector
        self.outdir = outdir

        self.model = None
        #Output file names:
        self.model_file = self.outdir + 'model_' + str(n_topics) + '.pkl'


    def vectorize(self):
        '''
        INPUT None
        OUTPUT TfidfVectorizer, TfidfVectorizer.fit_transform()

        If the vectorizer is not supplied, then this function creates
        TfidfVectorizer.
        '''
        if self.vectorizer is None:
            self.vectorizer = TfidfVectorizer(tokenizer=tokenize,
                                              max_features=self.n_features)
            self.vector = self.vectorizer.fit_transform(self.df.content).toarray()

            print 'Writing: ', self.outdir + 'vectorizer.pkl'
            with open(self.outdir + 'vectorizer.pkl', "wb") as f:
                pkl.dump((self.vectorizer, self.vector), f)

        return self.vectorizer, self.vector


    def build_model(self):
        self.vectorizer, self.vector = self.vectorize()
        self.model = NMF(n_components=self.n_topics).fit(self.vector)

        print "Writing: ", self.model_file
        pkl.dump(self.model, open(self.model_file, "wb"))


if __name__ == '__main__':
    n_topics = sys.argv[1:]

    vectorizer = None
    vector = None
    df = None

    try:
        #If the pickle file already exists, then load the vectorizer from pickle
        f = open("data/vectorizer.pkl")
        vectorizer, vector = pkl.load(f)
    except:
        df = pkl.load(open('data/data_all.pkl'))

    for n in n_topics:
        print "N topics:", n
        model = Model(n_topics=int(n), df=df, vectorizer=vectorizer, vector=vector)
        model.build_model()

    
