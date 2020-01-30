"""from dataop.es_tool import ElasticsearchTool
from analysis.topic import topic_modeling
if __name__ == '__main__':
    #index = input("index: ")
    #doc_type = input("type: ")
    index = 'cttw_clean'
    doc_type = 'tweet'
    host = ["127.0.0.1:9200"]
    et = ElasticsearchTool(host)
    #tweets = et.traverse_clean(index, doc_type)
    top = [{},{},{}]
    sen = []
    for days in range(28):
        start_date = "2019-02-"+str(days+1)
        end_date = "2019-02-"+str(days+2)
        if days+1 == 28:
            end_date = "2019-03-01"
        tweets = et.get_by_date_range_clean(index, doc_type, start_date,end_date)
        print(start_date, "--",end_date)
        print(len(tweets))
        topics = topic_modeling(tweets)
        day_sen = 0;
        for i in topics:
            total_sentiment_score = 0
            print("Topic "+ str(i)+": ")

            for t in topics[i]:
                if t[0] in top[i]:
                    top[i][t[0]] += 1
                else:
                    top[i][t[0]] = 1
                print(t[0])
                total_sentiment_score += float(t[1])

            avg_sentiment_score = total_sentiment_score / len(topics[i])
            day_sen += avg_sentiment_score
            print("Topic sentiment: ", avg_sentiment_score)
        day_sen/=len(topics)
        sen.append(day_sen)
    for i in top:
        for t in i:
            print(t,i[t])
    for i in sen:
        print(i)"""
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

def load_lexicon(lexicon):
    with open(lexicon) as f:
        lex = json.load(f)
    ret = {}
    ps = PorterStemmer()
    for key in lex:
        stemmed_words = []
        for w in lex[key]:
            stemmed_words.append(ps.stem(w))
        ret[key] = stemmed_words
    return ret
def load_lexicon_original(lexicon):
    with open(lexicon) as f:
        lex = json.load(f)
    return lex
def stem(text):
    tokenized_sent = word_tokenize(text)
    filtered_sent = []
    stop_words = set(stopwords.words("english"))
    for w in tokenized_sent:
        if w not in stop_words:
            filtered_sent.append(w)
    ps = PorterStemmer()
    stemmed_words = []
    for w in filtered_sent:
        stemmed_words.append(ps.stem(w))
    return stemmed_words

def catagorize(text,lex):
    topics = []
    text_stemmed = stem(text)
    for key in lex:
        checked = False
        for w in lex[key]:
            if(checked):
                break
            for t in text_stemmed:
                if(checked):
                    break
                if(t == w):
                    checked = True
                    topics.append(key)
    return topics

def find_match(text,lex):
    keyword = []
    text_stemmed = stem(text)
    ps = PorterStemmer()
    for key in lex:
        checked = False
        for w in lex[key]:
            if(checked):
                break
            for t in text_stemmed:
                if(checked):
                    break
                if(t == ps.stem(w)):
                    checked = True
                    keyword.append(w)
    separator = ', '

    return separator.join(keyword)
def tweets_match_keyword(tweets, lex):
    new_tweets = []
    counter = len(tweets)
    for t in tweets:
        counter -= 1
        # if counter <=56605:
        #     break
        print(counter)
        match = find_match(t['text'],lex)
        if match != '':
            print(match)
            new_tweets.append(match)
    return new_tweets
if __name__ == '__main__':
    lex = load_lexicon("semantic_lexicon.json")
    text = "Due to an incident on suspension 7th Ave, Trains will not be travelling on the Ave.  NW trains come into 8 St and turnaround, West trains will be turning around at 7 St.  South trains will be turning around at City Hall south platform and the NE trains will be turning at City Hall north"
    topcis = catagorize(text,lex)
    analyzer = NaiveBayesAnalyzer()
    b = TextBlob(text, analyzer=analyzer)
    sent = {
        'positive': b.sentiment.p_pos,
        'negative': b.sentiment.p_neg
    }
    print(sent)
    print(topcis)
