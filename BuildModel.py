import pandas as pd
import pickle as pkl

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

#from utils import stop_words, tokenize


class Model(object):
    def __init__(self, df, n_topics, n_features=5000, outdir='data/',
                 vectorizer=None, vector=None):
        self.n_features = n_features
        self.df = df
        self.n_topics = n_topics        
        self.vectorizer = vectorizer
        self.vector = vector

        self.model = None

        #Output dir and file names:
        self.outdir = outdir # current dir 
        self.model_file = self.outdir + 'model_' + str(n_topics) + '.pkl'


    def vectorize(self):
        if self.vectorizer is None:
            self.vectorizer = TfidfVectorizer(tokenizer=tokenize,
                                              max_features=self.n_features)
            print 'Writing: ', outdir + 'vectorizer.pkl'
            pkl.dump(self.vectorizer,
                     open(self.outdir + 'vectorizer.pkl', "wb"))


        if self.vector is None:
            self.vector = self.vectorizer.fit_transform(self.df.content).toarray()
            print 'Writing: ', outdir + 'vector.pkl'
            pkl.dump(self.vector,
                     open(self.outdir + 'vector.pkl', "wb"))

        return self.vectorizer, self.vector


    def build_model(self):
        self.vectorizer, self.vector = self.vectorize()
        self.model = NMF(n_components=self.n_topics).fit(self.vector)

        print "Writing: ", self.model_file
        pkl.dump(self.model, open(self.model_file, "wb"))


if __name__ == '__main__':

    df = pkl.load(open('data/data_all.pkl'))

    #model = Model(df, n_topics=30)

    vectorizer = pkl.load(open('data/vectorizer.pkl'))
    vector = pkl.load(open('data/vector.pkl'))

    model = Model(df, n_topics=50, vectorizer=vectorizer, vector=vector)

    # build only one model
    model.build_model()
