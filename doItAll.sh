
rm TopicBrowser/static/*
rm data/*

echo "MongoToDataFrame"
ipython MongoToDataFrame.py

echo "BuildModel"
ipython BuildModel.py

echo "WriteCSVs"
ipython WriteCSVs.py

echo "WordCloud"
ipython WordCloud.py
