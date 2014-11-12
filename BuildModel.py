import pandas as pd
import pickle as pkl

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

#from nltk import WordNetLemmatizer, word_tokenize

from MongoToDataFrame import MongoToDataFrame
from utils import stop_words, tokenize


class Model(object):
    def __init__(self, df, n_features=5000):
        self.n_features = n_features

        self.df = df

        self.vectorizer = None
        self.vector = None
        self.model = None

        '''
        Output dir and file names:
        '''
        self.outdir = "data/" # current dir 
        self.vect_file1 = self.outdir + "vectorizer.pkl"
        self.vect_file2 = self.outdir + "vectors.pkl"
        self.model_file = self.outdir + "model.pkl"


    def vectorize(self):
        vectorizer = TfidfVectorizer(tokenizer=tokenize,
                                     max_features=self.n_features)
        vector = vectorizer.fit_transform(self.df.content).toarray()
        return vectorizer, vector


    def build_model(self, n_topics):
        self.vectorizer, self.vector = self.vectorize()
        self.model = NMF(n_components=n_topics).fit(self.vector)


    def build_models(self, n_topics):
        '''
        INPUT list
        OUTPUT None
        '''
        self.model = []
        for n in n_topics:
            nmf = NMF(n_components=n).fit(self.vector)
            self.model.append(nmf)


    def pickle_model(self):
        if self.vector is not None:
            print "Writing: ", self.vect_file1
            pkl.dump(self.vectorizer, open(self.vect_file1, "wb"))
            print "Writing: ", self.vect_file2
            pkl.dump( self.vector, open(self.vect_file2, "wb"))

        if self.model is not None:
            print "Writing: ", self.model_file
            pkl.dump(self.model, open(self.model_file, "wb"))


    def pickle_models(self):
        if self.vector is not None:
            print "Writing: ", self.vect_file1
            pkl.dump(self.vectorizer, open(self.vect_file1, "wb"))
            print "Writing: ", self.vect_file2
            pkl.dump(self.vector, open(self.vect_file2, "wb"))

        prefix, ext = self.model_file.split('.')
        if self.model is not None and len(self.model) > 0:
            for i, model in self.model:
                outfile = prefix + "_" + str(i) + ".pkl"
                print "Writing: ", outfile
                pkl.dump(model, open(outfile, "wb"))



if __name__ == '__main__':

    df = MongoToDataFrame().get_data_frame()

    model = Model(df)

    # build only one model
    model.build_model(20) # 20 topics
    model.pickle_model()

    # build more that one models with different number of topics
    #n_topics = range(5,51,5)
    #model.build_models(n_topics)
    #model.pickle_models()
