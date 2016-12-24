import time
import json
from config import *
import markovify

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report

import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener

auth = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

traintweets = []
trainclass = []
testtweets = []
testclass = []
with open('posts.txt') as f:
    data = f.readlines()
    for i, a in enumerate(data):
        if i < len(data) * .9:
            traintweets.append(a)
        else:
            testtweets.append(a)
with open('classify.txt') as f:
    data = f.readlines()
    for i, a in enumerate(data):
        if i < len(data) * .9:
            trainclass.append(a)
        else:
            testclass.append(a)

# Create feature vectors
vectorizer = TfidfVectorizer(min_df=5,
                             max_df=0.8,
                             sublinear_tf=True,
                             use_idf=True)
trainvec = vectorizer.fit_transform(traintweets)
testvec = vectorizer.transform(testtweets)

# Perform classification with SVM, kernel=linear
classifier_liblinear = svm.LinearSVC()
t0 = time.time()
classifier_liblinear.fit(trainvec, trainclass)
t1 = time.time()
prediction_liblinear = classifier_liblinear.predict(testvec)
t2 = time.time()
time_liblinear_train = t1 - t0
time_liblinear_predict = t2 - t1

# Train Markov Chain
with open('encouraging.txt') as f:
    text = f.read()
text_model = markovify.Text(text)

print "Training time: %fs; Prediction time: %fs" % (time_liblinear_train, time_liblinear_predict)
print classification_report(testclass, prediction_liblinear)


class MyListener(StreamListener):
    def on_data(self, data):
        try:
            new = json.loads(data)['text'].replace('RT ', '')
            testvec = vectorizer.transform([new])
            prediction_liblinear = classifier_liblinear.predict(testvec)

            if 's' in prediction_liblinear[0]:
                user = json.loads(data)['user']['screen_name']
                api.update_status("@" + user + " " + text_model.make_short_sentence(138 - len(user)))

        except BaseException as e:
            print('&quot;Error on_data: %s&quot;' % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['anxiety', 'sadness', 'suicide', 'depression', 'sad'])
