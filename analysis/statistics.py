from PIL import Image
from dateutil.parser import parse
import wordcloud
import spacy
import numpy as np
from wordcloud import STOPWORDS
def temporal(tweets):
    dates = {}
    for t in tweets:
        d = parse(t['date']).date()
        d = d.replace(day = 1)
        #d = d.year*10000+d.month*100+d.day
        if d in dates:
            dates[d]+=1
        else:
            dates[d] = 1
    return sorted(dates.items(),key=lambda d:d[0])
def temporal_ids(tweets):
    id_date = {}
    for t in tweets:
        d = parse(t['date']).date()
        d = d.replace(day = 1)
        id = t['id']
        id_date[id]=d
    return sorted(id_date.items(),key=lambda d:d[1])
def likes(tweets):
    return sorted(tweets, key=lambda d: d['likes'], reverse=True)
def geoinfo(tweets):
    geo = {}
    for t in tweets:
        if t['geo'] in geo:
            geo[t['geo']]+=1
        else:
            geo[t['geo']] = 1
    return sorted(geo.items(), key=lambda d: d[1],reverse=True)
def hashtags(tweets):
    ht = {}
    for t in tweets:
        for h in t['hashtags']:
            hashtag = h['text'].lower()
            if hashtag in ht:
                ht[hashtag] += 1
            else:
                ht[hashtag] = 1
    return sorted(ht.items(), key=lambda d: d[1],reverse=True)
def get_statistics(tweets):
    print(len(tweets))
    geo = geoinfo(tweets)

def generate_wordcloud(tweets, fname_base):
    text = b" ".join((t['text'].encode('utf-8') for t in tweets)).lower().decode('utf-8')
    mk = np.array(Image.open('mk.png'))
    sw = set(STOPWORDS)
    sw.add("https")
    sw.add("CO")
    sw.add("self")
    wc = wordcloud.WordCloud(background_color='white',stopwords=sw,mask=mk,width=800, height=800).generate(text)
    wc.to_file('{}.jpg'.format(fname_base))


def generate_wordcloud_text(tweets_text, fname_base):
    text = b" ".join((t.encode('utf-8') for t in tweets_text)).lower().decode('utf-8')
    mk = np.array(Image.open('mk_text.png'))
    sw = set(STOPWORDS)
    wc = wordcloud.WordCloud(background_color='white',stopwords=sw,mask=mk,width=600, height=600).generate(text)
    wc.to_file('{}.jpg'.format(fname_base))