import hashlib
import random
import string

from mongoengine import *

class User(Document):
	name = StringField(required=True, max_length=100)
	username = StringField(required=True)
	password = StringField(required=True)
	salt = StringField(required=True)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.username

	def check_password_hash(self, form_password):
		m = hashlib.sha512()
		m.update(self.salt)
		m.update(form_password)
		return self.password == m.hexdigest()

def create_user(name, username, password):
	# Generate random salt
	salt = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for i in range(0, 15))

	# Generate password hash
	m = hashlib.sha512()
	m.update(salt)
	m.update(password)
	password_hash = m.hexdigest()

	return User(name=name, username=username, password=password_hash, salt=salt)

class Tweet(Document):
	name = StringField(required=True)
	handle = StringField(required=True)
	date = LongField(required=True)
	num_retweets = IntField(required=True)
	location = PointField(required=True, null=True)
	content = StringField(required=True)
	risk_level = IntField(required=True)