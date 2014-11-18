# Tech Chatter in the News
### Capstone Project, Zipfian Academy

This project is focused on discovering abstract topics in technology news using topic modeling algorithms, and observing the evolution of these topics over time.  

I used technology news articles from New York Times for last few years. These articles were categorized into different topics using Non-Negative Factorization technique in topic modeling. To visualize the results of the model, an interactive topic browser was developed using d3.  

####Data
Almost 7000 technology articles were scraped from NYT website. First, the headlines and web urls of news articles were obtained using NYT API. Using these web urls, individual articles were collected and saved in mongo database. For several articles obtained from the API, the actual contents were not present on NYT website, because these articles were sourced by either Reuters or Associated Press. I was able to get some of the missing articles from Reuters website, but Associated Press articles were not collected because there wasn't any simpler way to find these on their website.  

####Topic Browser
The topic browser is a web app which shows the results of topic modeling in a very compact and efficient way. The description and the demo of this app can be found [here](http://iyounus.github.io/).  

####Code
The shell script `do_it_all.sh` provides simple pipeline to create the necessary data for the web app. It take one parameter, number of topics, as input which is needed for NMF. It, then, runs the following modules in the given sequence:  

```
1- mongo_to_dataframe.py   
2- build_model.py  
3- web_app_data.py  
4- word_cloud.py  
```
The first module reads mongo db and creates a pandas datafram (which is stored as pickle file). The second module loads the dataframs and fits NMF model to the text content of articlels to identify topics. The model and the tf-idf vectorizer, created in this module, are also saved as pickle files. The 3rd and the 4th modules take the dataframe and the fitted model from the pickle files and create necessary data files and word cloud images for the web app.  

The `index.html` file in the topic_browser folder reads the csv and image files created by above modules and displays the results using interactive graphics.  
