import pandas as pd
import pickle as pkl

from pymongo import MongoClient


class MongoToDataFrame(object):
    def __init__(self):
        self.collection = self.init_mongo()
        self.df = self.create_df()


    def init_mongo(self):
        '''
        INPUT None
        OUPUT collection

        This function reads mongodb, nyt_tech, for NYT articles and
        returns collection articles
        '''
        client = MongoClient()
        db = client.nyt_tech
        return db.articles


    def create_df(self):
        '''
        INPUT None
        OUPUT DataFrame

        Reads mongodb and inserts the required fields in DataFrame
        '''
        columns = ['web_url','headline','section_name','pub_date','content']
        d = {col : [] for col in columns}

        for article in self.collection.find({'content' : {'$exists' : True}}):
            # Only get articles for 2014, this is temporary
            if '2014' in article['pub_date']:
                for col in columns:
                    if col == 'headline': # headline is a dict
                        d[col].append(article[col]['main'])
                    else:
                        d[col].append(article[col])

        return pd.DataFrame(d)


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
    m2df.save_pickle_df("data/nyt_data.pkl")
