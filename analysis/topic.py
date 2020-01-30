import pandas as pd

from tweet_parser.tweet import Tweet
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from nltk.corpus import stopwords

def topic_modeling(tweets):
    documents = []
    for t in tweets:
        documents.append(t['text'])

    news_df = pd.DataFrame({'document':documents})
    news_df['clean_doc'] = news_df['document'].str.replace("[^a-zA-Z#]", " ")
    news_df['clean_doc'] = news_df['clean_doc'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>3]))
    news_df['clean_doc'] = news_df['clean_doc'].apply(lambda x: x.lower())

    stop_words = stopwords.words('english')
    tokenized_doc = news_df['clean_doc'].apply(lambda x: x.split())
    tokenized_doc = tokenized_doc.apply(lambda x: [item for item in x if item not in stop_words])
    detokenized_doc = []

    for i in range(len(news_df)):
        t = ' '.join(tokenized_doc[i])
        detokenized_doc.append(t)
    news_df['clean_doc'] = detokenized_doc


    vectorizer = TfidfVectorizer(stop_words='english',
                                 max_features= 1000, # keep top 1000 terms
                                 max_df = 0.5,
                                 smooth_idf=True)
    X = vectorizer.fit_transform(news_df['clean_doc'])
    print(X.shape)
    # print(X)
    # print(type(X))

    svd_model = TruncatedSVD(n_components=3, algorithm='randomized', n_iter=100, random_state=122)
    svd_model.fit(X)

    print(len(svd_model.components_))

    terms = vectorizer.get_feature_names()
    topics = {}
    for i, comp in enumerate(svd_model.components_):
        terms_comp = zip(terms, comp)
        sorted_terms = sorted(terms_comp, key= lambda x:x[1], reverse=True)[:7]
        topics[i] = sorted_terms

    return topics


