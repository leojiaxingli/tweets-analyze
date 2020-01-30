import json
import sys
import re
import copy
import datetime

from tweet_parser.tweet import Tweet
from dateutil import rrule as drule
import dateutil.parser as dp
from dateutil.relativedelta import relativedelta

from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

import wordcloud
import spacy

def load_tweets(fn):
    with open(fn) as f:
        tweets = json.load(f)
    return [Tweet(t) for t in tweets]

def sentiment(t, analyzer=None):
    if analyzer is None:
        analyzer = NaiveBayesAnalyzer()
    b = TextBlob(t['text'], analyzer=analyzer)
    return {
        'positive': b.sentiment.p_pos,
        'negative': b.sentiment.p_neg
    }
def text_sentiment(text):
    analyzer = NaiveBayesAnalyzer()
    b = TextBlob(text, analyzer=analyzer)
    return {
        'positive': b.sentiment.p_pos,
        'negative': b.sentiment.p_neg
    }
def topic_sentiment(topic, analyzer=None):
    if analyzer is None:
        analyzer = NaiveBayesAnalyzer()
    b = TextBlob(topic, analyzer=analyzer)
    return {
        'positive': b.sentiment.p_pos,
        'negative': b.sentiment.p_neg,
        'neutral': 0
    }
def avg_sentiment(tweets):
    pos, neg, neu = 0, 0, 0
    analyzer = NaiveBayesAnalyzer()
    for t in tweets:
        res = sentiment(t, analyzer=analyzer)
        pos += res['positive']
        neg += res['negative']
        neu += res['neutral']
    if tweets:
        l = len(tweets)
        return pos/l, neg/l, neu/l

def get_by_date_range(tweets, from_date, to_date, inclusive=True):
    if isinstance(from_date, str):
        from_date = dp.parse(from_date).date()
    if isinstance(to_date, str):
        to_date = dp.parse(to_date).date()

    if isinstance(from_date, datetime.datetime):
        from_date = from_date.date()
    if isinstance(to_date, datetime.datetime):
        to_date = to_date.date()

    res = []
    for t in tweets:
        d = dp.parse(t['date']).date()
        if from_date <= d:
            if (inclusive and d <= to_date) or \
               (not inclusive and d < to_date):
                res.append(copy.deepcopy(t))

    #return [copy.deepcopy(t) for t in tweets if from_date <= dp.parse(t['date']).date() <= to_date]
    return res

def generate_months(start, stop, interval=None, both=True):
    if isinstance(start, datetime.datetime):
        start = start.date()+relativedelta(day=1)
    if isinstance(stop, datetime.datetime):
        stop = stop.date()+relativedelta(day=1)

    args = {
        'dtstart': start,
        'until': stop,
        # 'bymonthday': 1
    }
    if both:
        args['bymonthday'] = [1, -1]
    if interval:
        args['interval'] = interval

    months = list(drule.rrule(drule.MONTHLY, **args))

    if both:
        if months[0].month != months[1].month:
            months.insert(0, months[0]+relativedelta(day=1))
        if months[-1].month != months[-2].month:
            months.append(months[-1]+relativedelta(day=1, months=1, days=-1))

    return months

def avg_sentiment_by_month(tweets):
    dates = sorted([dp.parse(t['date']) for t in tweets])
    start, end = dates[0], dates[-1]
    months = generate_months(start, end)

    results = []
    i = 0

    while i < len(months)-1:
        st, en = months[i], months[i+1]
        month_str = st.strftime("%B %Y")
        twts = get_by_date_range(tweets, st, en)
        pos, neg, _ = avg_sentiment(twts)
        results.append({
            "month": month_str,
            "tweets": len(twts),
            "positive": pos,
            "negative": neg
        })

        i += 2

    return results
if __name__ == '__main__':
    print(topic_sentiment("test"))