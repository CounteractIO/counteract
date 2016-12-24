from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import json
import urllib
import random
import csv
import config


def my_shuffle(array):
    random.shuffle(array)
    return array


# Access tokens
auth = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)
# Get training tweets

tweets = []

# happy= 1
# sad = 0

for tweet in tweepy.Cursor(api.search,
                           q="anxiety",
                           lang="en").items(100):
    # Write a row to the csv file/ I use encode utf-8
    tweets.append([tweet.text.replace('\n', ' ').encode('utf-8'), '0'])

for tweet in tweepy.Cursor(api.search,
                           q="depression",
                           lang="en").items(100):
    # Write a row to the csv file/ I use encode utf-8
    tweets.append([tweet.text.replace('\n', ' ').encode('utf-8'), '0'])

for tweet in tweepy.Cursor(api.search,
                           q="good",
                           lang="en").items(100):
    # Write a row to the csv file/ I use encode utf-8
    tweets.append([tweet.text.replace('\n', ' ').encode('utf-8'), '1'])

for tweet in tweepy.Cursor(api.search,
                           q="1",
                           lang="en").items(100):
    # Write a row to the csv file/ I use encode utf-8
    tweets.append([tweet.text.replace('\n', ' ').encode('utf-8'), '1'])

for tweet in tweepy.Cursor(api.search,
                           q="suicide",
                           lang="en").items(100):
    # Write a row to the csv file/ I use encode utf-8
    tweets.append([tweet.text.replace('\n', ' ').encode('utf-8'), '0'])

for tweet in tweepy.Cursor(api.search,
                           q="great",
                           lang="en").items(100):
    # Write a row to the csv file/ I use encode utf-8
    tweets.append([tweet.text.replace('\n', ' ').encode('utf-8'), '1'])

f = open('tweets.txt', 'w')

towrite = my_shuffle(tweets)
print towrite[0]

for tweet in towrite:
    tweetfile = open('posts.txt', 'a')
    classifyfile = open('classify.txt', 'a')
    tweetfile.write(tweet[0] + '\n')
    classifyfile.write(tweet[1] + '\n')

alltweets = []
# Get encouraging tweets
new_tweets = api.user_timeline(screen_name='Words2Encourage', count=200)

# save most recent tweets
alltweets.extend(new_tweets)

# save the id of the oldest tweet less one
oldest = alltweets[-1].id - 1

# keep grabbing tweets until there are no tweets left to grab
while len(new_tweets) > 0:
    print "getting tweets before %s" % (oldest)

    # all subsiquent requests use the max_id param to prevent duplicates
    new_tweets = api.user_timeline(screen_name='Words2Encourage', count=200, max_id=oldest)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # update the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    print "...%s tweets downloaded so far" % (len(alltweets))

# transform the tweepy tweets into a 2D array that will populate the csv
outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

# write the csv
with open('%s_tweets.csv' % 'Words2Encourage', 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(["id", "created_at", "text"])
    writer.writerows(outtweets)

pass
