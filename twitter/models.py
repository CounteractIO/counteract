from mongoengine import *

class Tweet(Document):
	name = StringField(required=True)
	handle = StringField(required=True)
	date = DateTimeField(required=True)
	num_retweets = IntField(required=True)
	location = PointField(required=True, null=True)
	content = StringField(required=True)
	risk_level = IntField(required=True)