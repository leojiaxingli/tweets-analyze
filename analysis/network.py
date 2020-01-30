CONSUMER_KEY = 'LgHaTAhcLzNyLcWRZPovwERAi'
CONSUMER_SECRET = 'e8MhS8arQQIUfS6URkPoJyeoZV24CS25RG3zwuKuK5CjnYVICE'
ACCESS_KEY = '1084522443815809024-H2Sr0QZN247OZSyuhpYigUjkuvyh2F'
ACCESS_SECRET = 'R6gXvu6EnRLHMKfIYCry79Mh98RghgAnximHDmSUNpkfa'

import tweepy
import networkx as nx
import matplotlib.pyplot as plt
import json
from tweepy import OAuthHandler

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def get_usernames(userids, api):
    fullusers = []
    u_count = len(userids)
    print(u_count)
    try:
        for i in range(int(u_count / 100) + 1):
            end_loc = min((i + 1) * 100, u_count)
            fullusers.extend(
                api.lookup_users(user_ids=userids[i * 100:end_loc])
            )
        return fullusers
    except:
        import traceback
        traceback.print_exc()
        print('Something went wrong, quitting...')
def get_followers(username, limit):
    followerids = []
    c = 0
    try:
        for user in tweepy.Cursor(api.followers_ids, screen_name=username, count=5000).items():
            c = c + 1
            if c > limit:
                break
            followerids.append(user)
    except tweepy.TweepError:
        print("Failed to run the command on that user, Skipping...")
    fullusers = get_usernames(followerids, api)
    allfollowers = []
    if fullusers == None:
        return []
    for user in fullusers:
        # print(counter)
        temp = (user._json)
        allfollowers.append(temp["screen_name"])
        #print("Twitter Handle: ", temp["screen_name"])
        # print("Followers:", temp["followers_count"])
        # print("Follows:", temp["friends_count"])
        # print("Number of tweets:", temp["statuses_count"])
        # print("\n" + "-------------------------" + "\n")
    return allfollowers
def get_network(ego):
    G = nx.Graph()
    initlal_fol = get_followers(ego,30)
    with open('{}.json'.format(ego), 'w') as outfile:
        json.dump(initlal_fol, outfile)
    G.add_node(ego)
    core_list = []
    for user in initlal_fol:
        G.add_node(user)
        G.add_edge(user,ego)
        fol_of_fol = get_followers(user,40)
        if fol_of_fol==None:
            continue
        with open('{}.json'.format(user), 'w') as outfile:
            json.dump(fol_of_fol, outfile)
        for fol in fol_of_fol:
            G.add_node(fol)
            G.add_edge(fol,user)

    nx.draw(G, with_labels= True)
    plt.draw()
    plt.show()
