import random
import string
import json

from datetime import datetime

from models import Tweet

from mongoengine import connect

from config import MONGODB_NAME, MONGODB_URI

connect(MONGODB_NAME, host=MONGODB_URI)

def seed_tweets():
    tweets = []

    # Generate 100 random tweets
    for i in range(1000):
        name = ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(6)) + ' ' + ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(6))
        handle = ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(8))

        # Generate random datetime within the last 48 hours
        today = datetime.today()
        start_date = today.replace(day=today.day - 4).toordinal()
        end_date = today.toordinal()
        date = datetime.fromordinal(random.randint(start_date, end_date))

        num_likes = random.randint(0, 200)
        num_retweets = random.randint(0, 50)

        location = [random.uniform(-180, 180), random.uniform(-90, 90)]

        content = ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(140))

        risk_level = random.uniform(0, 100)

        tweet = Tweet(name=name, handle=handle, date=date, num_likes=num_likes, num_retweets=num_retweets, location=location, content=content, risk_level=risk_level)
        tweet.save()
        #tweets.append(json.loads(tweet.to_json()))

    '''f = open('static/js/tweets.json', 'w')
    f.write(json.dumps(tweets))
    f.close()'''

seed_tweets()