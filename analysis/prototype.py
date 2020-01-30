import os
import json
import csv
import matplotlib.pyplot as plt
import numpy as np
import prettytable as pt
import datetime
from dateutil.parser import parse

from analysis.statistics import *
from analysis.semantic import *
from analysis.sentiment import *
from analysis.network_offline import get_network
def plot(title,xlabel,ylabel,x_data,y_data,y1legend):
    bar_width = 0.3

    plt.bar(x=x_data, height=y_data, label=y1legend,
            color='steelblue', alpha=0.8, width=bar_width)

    plt.xticks(x_data, x_data, rotation=20)
    for a, b in zip(x_data, y_data):
        plt.text(a, b, '%.0f' % b, ha='center', va='bottom', fontsize=17)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

def plot2(title,xlabel,ylabel,x_data,y_data,y_data2,y1legend,y2legend):
    bar_width = 0.3

    plt.bar(x=x_data, height=y_data, label=y1legend,
            color='steelblue', alpha=0.8, width=bar_width)

    plt.xticks(x_data, x_data, rotation=20)

    for a, b in zip(x_data, y_data):
        plt.text(a, b, str(round(b,2)), ha='center', va='bottom', fontsize=17)

    plt.bar(x=np.arange(len(x_data)) + bar_width, height=y_data2,
        label=y2legend, color='indianred', alpha=0.8, width=bar_width)
    for a, b in enumerate(y_data2):
        plt.text(a+bar_width, b, str(round(b,2)), ha='center', va='bottom', fontsize=17)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()
def plot2_line(title,xlabel,ylabel,x_data,y_data,y_data2,y1legend,y2legend):
    plt.plot(x_data, y_data,'ro-', color='steelblue', alpha=0.8, label=y1legend)
    plt.plot(x_data, y_data2, 'bs-', color='indianred', alpha=0.8, label=y2legend)
    plt.xticks(x_data, x_data, rotation=20)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()
def clean(t):
    # mentions
    tn = re.sub(r'@[A-Za-z0-9]+', '', t)
    # urls
    tn = re.sub(r'https?://[A-Za-z0-9./]+', '', tn)
    # numbers
    tn = re.sub(r'[0-9]+', '', tn)
    # other chars
    to_remove = '#$%^&*()_+=[]{}|\\<>/-:;`~"'
    tn = ''.join(c for c in tn if c not in to_remove)
    return " ".join(tn.split())
def plot_sem_sent(tweets,lex):
    topics = {}
    topics_pos = {}
    topics_neg = {}
    for key in lex:
        topics[key] = 0
        topics_pos[key] = 0
        topics_neg[key] = 0
    topics['None'] = 0
    topics_pos['None'] = 0
    topics_neg['None'] = 0
    all_pos = 0
    all_neg = 0
    sent_counter = 1
    counter = len(tweets)
    new_tweets = []
    for t in tweets:
        counter -= 1
        print(counter)
        # topic = catagorize(t['text'],lex)
        topic = find_match(t['text'],lex)
        sent = {'positive': 0,'negative': 0}
        if len(topic)>0:
            sent_counter += 1
            # sent = text_sentiment(t['text'])
            all_pos += sent['positive']
            all_neg += sent['negative']
            t['sentiment']['positive'] = sent['positive']
            t['sentiment']['negative'] = sent['negative']
            for to in topic:
                t['semantic'].append(to)
                topics[to] = topics[to] + 1
                topics_pos[to] += sent['positive']
                topics_neg[to] += sent['negative']
        else:
            topics['None'] = topics['None'] + 1
            #topics_pos['None'] += sent['positive']
            #topics_neg['None'] += sent['negative']
        new_t = {}
        new_t['id'] = t['id']
        new_t['sent'] = sent
        new_t['topics'] = topic
        new_tweets.append(new_t)
    all_pos /= sent_counter
    all_neg /= sent_counter
    for k in topics:
        if not topics[k] == 0:
            topics_pos[k] /= topics[k]
            topics_neg[k] /= topics[k]
    print(topics)
    print(topics_pos)
    print(topics_neg)
    print(str(all_pos)+","+str(all_neg))

    x_data = []
    y_data = []
    y_sent_pos = []
    y_sent_neg = []
    for k in topics:
        x_data.append(k)
        y_data.append(topics[k])
        y_sent_pos.append(topics_pos[k])
        y_sent_neg.append(topics_neg[k])
    # with open('{}.json'.format('xxx'), 'w') as outfile:
    #     json.dump(new_tweets, outfile)

    plot('Topics','Topic','Number',x_data,y_data,'Number')

    plot2('Sentiment','Topic','Sentiment',x_data,y_sent_pos,y_sent_neg,'Positive','Negative')

def extract(t):
    geo = t['user']['location']
    if geo == '':
        geo = 'Unknown'
    return {
        'id':t['id'],
        'text':t['text'],
        'date':t['created_at'],
        'geo':geo,
        'likes':t['favorite_count'],
        'hashtags':t['entities']['hashtags'],
        'sentiment':{'positive':0,'negative':0},
        'semantic':[],
        'owner':''
    }
def plot_hashtags(tweets,max_num):
    ht = hashtags(tweets)
    x_data = []
    y_data = []
    counter = 0
    for h, num in ht:
        x_data.append(h)
        y_data.append(num)
        counter += 1
        if counter > max_num:
            break
    plot('Hashtags Distribution (Top {})'.format(max_num), 'Hashtag', 'Number', x_data, y_data, 'Number')

def plot_geo(tweets,max_num):
    geo = geoinfo(tweets)
    x_data = []
    y_data = []
    counter = 0
    for loc,num in geo:
        if loc=='Unknown':
            continue
        x_data.append(loc)
        y_data.append(num)
        counter+=1
        if counter >max_num+1:
            break
    plot('Geographic Distribution (Top {})'.format(max_num), 'Location', 'Number', x_data, y_data, 'Number')
def print_likes(tweets,max_num):
    l = likes(tweets)
    counter = 0
    tb = pt.PrettyTable( ["Text", "Likes"])
    for t in  l:
        tb.add_row([t['text'],t['likes']])
        counter+=1
        if counter >max_num:
            break
    print(tb)
def plot_temporal(tweets,start,end):
    start = parse(start).date()
    end = parse(end).date()
    temp = temporal(tweets)
    x_data = []
    y_data = []
    for t,num in temp:
        if t>=start and t<=end:
            x_data.append(t)
            y_data.append(num)
    plot('Temporal Distribution (From: {} To: {})'.format(start, end), 'Month', 'Number', x_data, y_data, 'Number')
def plot_sem_sent_offline(file,lex):
    topics_num = {}
    topics_pos = {}
    topics_neg = {}
    for key in lex:
        topics_num[key] = 0
        topics_pos[key] = 0
        topics_neg[key] = 0
    topics_num['None'] = 0
    topics_pos['None'] = 0
    topics_neg['None'] = 0
    all_pos = 0
    all_neg = 0
    sent_counter = 1
    with open("{}".format(file)) as tw:
        tweets = json.load(tw)
        for t in tweets:
            topic = t['topics']
            sent = t['sent']
            if len(topic)>0:
                sent_counter += 1
                all_pos += sent['positive']
                all_neg += sent['negative']
                for to in topic:
                    topics_num[to] += 1
                    topics_pos[to] += sent['positive']
                    topics_neg[to] += sent['negative']
            else:
                topics_num['None'] = topics_num['None'] + 1

    all_pos /= sent_counter
    all_neg /= sent_counter
    for k in topics_num:
        if not topics_num[k] == 0:
            topics_pos[k] /= topics_num[k]
            topics_neg[k] /= topics_num[k]
    print(topics_num)
    print(topics_pos)
    print(topics_neg)
    print("Overall: ",str(all_pos)+","+str(all_neg))

    x_data = []
    y_data = []
    for k in topics_num:
        x_data.append(k)
        y_data.append(topics_num[k])
    plot('Topics','Topic','Number',x_data,y_data,'Number')

    x_data = []
    y_sent_pos = []
    y_sent_neg = []
    for k in topics_num:
        if k!="None":
            x_data.append(k)
            y_sent_pos.append(topics_pos[k])
            y_sent_neg.append(topics_neg[k])

    x_data.append("Overall")
    y_sent_pos.append(all_pos)
    y_sent_neg.append(all_neg)
    plot2('Sentiment','Topic','Sentiment',x_data,y_sent_pos,y_sent_neg,'Positive','Negative')
def temporal_vs_sent(tweets,start,end,file):
    start = parse(start).date()
    end = parse(end).date()
    temp_ids = temporal_ids(tweets)


    date_pos = {}
    date_neg = {}
    date_num = {}
    with open("{}".format(file)) as tw:
        tweets = json.load(tw)
        for id, date in temp_ids:
            if date >= start and date <= end:
                if date not in date_pos:
                    date_pos[date] = 0
                if date not in date_neg:
                    date_neg[date] = 0
                if date not in date_num:
                    date_num[date] = 0

                pos = tweets[str(id)]['sent']['positive']
                neg = tweets[str(id)]['sent']['negative']
                if pos != 0 and neg !=0:
                    date_pos[date]+=pos
                    date_neg[date]+=neg
                    date_num[date]+=1
    x_data = []
    y_sent_pos = []
    y_sent_neg = []
    for d in date_num:
        num = date_num[d]
        if num == 0:
            num = 1
        x_data.append(str(d))
        y_sent_pos.append(date_pos[d]/num)
        y_sent_neg.append(date_neg[d]/num)
    plot2_line('Sentiment vs Time', 'Month', 'Sentiment', x_data, y_sent_pos, y_sent_neg, 'Positive', 'Negative')
    with open('csv//sent_temp.csv', 'w',errors='ignore')as f:
        f_csv = csv.writer(f)
        f_csv.writerow(x_data)
        f_csv.writerow(y_sent_pos)
        f_csv.writerow(y_sent_neg)
def prototype():
    # lex = load_lexicon("semantic_lexicon.json")
    lex = load_lexicon_original("json//semantic_lexicon.json")

    tweets = []
    for root, dirs, files in os.walk("tweets"):
        for f in files:
            with open("tweets//{}".format(f)) as tw:
                all_tweets = json.load(tw)
                for t in all_tweets:
                    et = extract(t)
                    et['owner'] = f.split('.')[0]
                    tweets.append(et)

    # plot_sem_sent(tweets,lex)
    tweets_match = tweets_match_keyword(tweets, lex)
    print(len(tweets))
    print(len(tweets_match))
    generate_wordcloud_text(tweets_match,"aaa")
    #sem_sent_csv("offline.json",lex)
    # for y in range(2016,2020):
    #     for m in range(1,13,3):
    #         plot_temporal(tweets,'{}-{}-1'.format(y,m),'{}-{}-1'.format(y,m+2))

    # plot_temporal(tweets, '2016-1-1', '2016-3-1')
    # print_likes(tweets,10)
    # plot_geo(tweets, 10)
    # plot_hashtags(tweets,100)
    # plot_sem_sent_offline("offline.json",lex)
    #print(keyword_frequency(tweets))
    # temporal_vs_sent(tweets,'2014-1-1','2020-10-1',"offline_dict.json")
def reformat():
    new_tweets = {}
    with open("{}".format("json//offline.json")) as tw:
        tweets = json.load(tw)
        for t in tweets:
            id = t['id']
            topic = t['topics']
            sent = t['sent']
            new_tweets[id] = {'topics':topic,'sent':sent}
    with open('json//{}.json'.format('abccc'), 'w') as outfile:
        json.dump(new_tweets, outfile)
def sem_geo_time():
    headers = ['id', 'date', 'geo', 'topics']
    rows = []
    tweets = []
    for root, dirs, files in os.walk("tweets"):
        for f in files:
            with open("tweets//{}".format(f)) as tw:
                all_tweets = json.load(tw)
                for t in all_tweets:
                    et = extract(t)
                    et['owner'] = f.split('.')[0]
                    tweets.append(et)

    with open("{}".format("json//offline_dict.json")) as tw:
        tts = json.load(tw)
        for t in tweets:
            id = t['id']
            row = [t['id'],t['date'],t['geo']]
            topic_str = ""
            counter = len(tts[str(id)]['topics'])-1
            for to in tts[str(id)]['topics']:
                topic_str+=to
                if counter > 0:
                    topic_str+=" & "
                counter -= 1
            if topic_str!="":
                row.append(topic_str)
                rows.append(row)
    for r in rows:
        for rrr in r:
            print(rrr,",",end="")
        print("")
    print(len(rows))
    with open('csv//test.csv', 'w',errors='ignore')as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rows)
def sem_sent_csv(file,lex):
    topics_num = {}
    topics_pos = {}
    topics_neg = {}
    for key in lex:
        topics_num[key] = 0
        topics_pos[key] = 0
        topics_neg[key] = 0
    topics_num['None'] = 0
    topics_pos['None'] = 0
    topics_neg['None'] = 0
    all_pos = 0
    all_neg = 0
    sent_counter = 1
    with open("{}".format(file)) as tw:
        tweets = json.load(tw)
        for t in tweets:
            topic = t['topics']
            sent = t['sent']
            if len(topic)>0:
                sent_counter += 1
                all_pos += sent['positive']
                all_neg += sent['negative']
                for to in topic:
                    topics_num[to] += 1
                    topics_pos[to] += sent['positive']
                    topics_neg[to] += sent['negative']
            else:
                topics_num['None'] = topics_num['None'] + 1

    all_pos /= sent_counter
    all_neg /= sent_counter
    for k in topics_num:
        if not topics_num[k] == 0:
            topics_pos[k] /= topics_num[k]
            topics_neg[k] /= topics_num[k]
    print(topics_num)
    print(topics_pos)
    print(topics_neg)
    print("Overall: ",str(all_pos)+","+str(all_neg))

    x_data = []
    y_data = []
    for k in topics_num:
        x_data.append(k)
        y_data.append(topics_num[k])
    plot('Topics','Topic','Number',x_data,y_data,'Number')



    x_data = []
    y_sent_pos = []
    y_sent_neg = []
    for k in topics_num:
        if k!="None":
            x_data.append(k)
            y_sent_pos.append(topics_pos[k])
            y_sent_neg.append(topics_neg[k])

    x_data.append("Overall")
    y_sent_pos.append(all_pos)
    y_sent_neg.append(all_neg)
    plot2('Sentiment','Topic','Sentiment',x_data,y_sent_pos,y_sent_neg,'Positive','Negative')
def wordcloud_out():
    with open("json//wd_offline.json") as f:
        tweets_match = json.load(f)
        generate_wordcloud_text(tweets_match, "aaa")
if __name__ == '__main__':
    wordcloud_out()
