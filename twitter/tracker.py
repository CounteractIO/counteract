import tweepy
from geopy.geocoders import Nominatim

import random

from config import *
from mongoengine import connect
from models import Tweet

connect(MONGODB_NAME, host=MONGODB_URI)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

user = api.get_user(username)

# Geolocator to convert address to coordinates
geolocator = Nominatim()

class ViolentStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        name = status.author.name
        handle = status.author.screen_name
        date = status.created_at
        num_retweets = status.retweet_count
        location = status.coordinates
        if location is None and status.place is not None:
            place = geolocator.geocode(status.place.full_name)
            location = [place.longitude, place.latitude]
        content = status.text
        risk_level = random.uniform(70, 90)
        new_tweet = Tweet(name=name, handle=handle, date=date, num_retweets=num_retweets, location=location, content=content, risk_level=risk_level)
        new_tweet.save()

stream_listener = ViolentStreamListener()
stream = tweepy.Stream(auth = api.auth, listener=stream_listener)
stream.filter(follow=[str(user.id)])