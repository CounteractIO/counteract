import random
import string
import json

from datetime import datetime

from models import Tweet

from mongoengine import connect

from config import MONGODB_NAME, MONGODB_URI

connect(MONGODB_NAME, host=MONGODB_URI)

def seed_tweets():
    # Delete all previously generated tweets
    Tweet.objects().delete()

    # Generate 500 random tweets
    for i in range(500):
        name = ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(6)) + ' ' + ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(6))
        handle = ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(8))

        # Generate random datetime within the last 48 hours
        today = datetime.today()
        start_date = today.replace(day=today.day - 4).toordinal()
        end_date = today.toordinal()
        date = int(datetime.fromordinal(random.randint(start_date, end_date)).strftime('%s')) * 1000
        num_retweets = random.randint(0, 50)

        # Only choose coordinates located on land
        america = [random.uniform(-120, -75), random.uniform(30, 60)]
        south_america = [random.uniform(-75, -60), random.uniform(-45, 0)]
        africa = [random.uniform(15, 30), random.uniform(-30, 30)]
        europe = [random.uniform(-10, 30), random.uniform(40, 55)]
        asia = [random.uniform(30, 135), random.uniform(23, 67)]
        location = random.choice([america, south_america, africa, europe, asia])

        content = ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(140))

        risk_level = random.uniform(0, 100)

        tweet = Tweet(name=name, handle=handle, date=date, num_retweets=num_retweets, location=location, content=content, risk_level=risk_level)
        tweet.save()

seed_tweets()