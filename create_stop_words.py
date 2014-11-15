from nltk.corpus import stopwords

def stop_words()
    '''
    INPUT None
    OUTPUT None

    This functions takes the stopwords in nltk package and add some more
    words to it.
    '''
    stop = stopwords.words('english')
    # some extra stop words not present in stopwords
    stop += ['said', 'would', 's', 'also', 'u', 'mr', 're', 'may', 'one',\
             'two', 'buy', 'much', 'take', 'might', 'say', 'new', 'year',
             'many', 'reporting', 'editing']

    return sorted(set(stop))


if __name__=="__main__":
    f = open("stop_words.txt","w")
    for word in stop_words():
        f.write("%s\n" % word)
