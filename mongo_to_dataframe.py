import pandas as pd
import pickle as pkl

from pymongo import MongoClient


class MongoToDataFrame(object):

    def __init__(self):
        self.mongo_client = MongoClient()
        # these columns will be stored in the output dataframe
        self.columns = ['web_url','headline','pub_date','content']
        self.data = {col : [] for col in self.columns}
        self.df = None

    def create_dict(self, db_name):
        '''
        INPUT None
        OUPUT DataFrame

        Reads mongodb and inserts the required fields in a dict
        '''
        collection = self.mongo_client[db_name]['articles']

        for article in collection.find({'content' : {'$exists' : True}}):
            #if '2014' not in article['pub_date']: continue
            for col in self.columns:
                if db_name=='nyt_tech' and col=='headline': # headline is a dict
                    self.data[col].append(article[col]['main'])
                else:
                    self.data[col].append(article[col])

        return self.data


    def create_df(self):
        self.create_dict('nyt_tech')
        self.create_dict('reuters')
        self.df = pd.DataFrame(self.data)
        # there are some duplicates in the db, so drop these here before further analysis
        self.df.drop_duplicates('web_url', inplace=True)

        self.df['headline_lower'] = self.df['headline'].map(lambda x : x.lower())
        self.df.drop_duplicates('headline_lower', inplace=True)
        del self.df['headline_lower']

        #temporarily store only data for last three years
        self.df['pub_date'] = pd.to_datetime(self.df['pub_date'])
        self.df = self.df[self.df['pub_date'] > "2011-12-31"]
        return self.df


    def save_pickle_df(self, out_file):
        '''
        INPUT String
        OUPUT None
        '''
        pkl.dump(self.df, open(out_file, "wb"))


    def get_data_frame(self):
        return self.df


if __name__ == '__main__':
    m2df = MongoToDataFrame()
    m2df.create_df()
    m2df.save_pickle_df("data/data_all.pkl")
