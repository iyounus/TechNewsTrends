
import pandas as pd
import pickle as pkl

from topic_ana import read_mongo


'''
This code snippet reads monog and creates a dataframe, then saves it as pickle.
'''

pkl_file = "data/nyt_data.pkl"
df = read_mongo()
pkl.dump(df, open(pkl_file, "wb"))
