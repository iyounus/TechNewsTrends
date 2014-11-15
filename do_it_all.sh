#!/bin/bash


echo "number of topics: " $1

echo "mongo_to_dataframe"
ipython mongo_to_dataframe.py

echo "build_model"
ipython build_model.py  $1

echo "write_web_app_csv"
ipython write_web_app_csv.py $1

echo "word_cloud"
ipython word_cloud.py $1
