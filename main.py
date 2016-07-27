from flask import Flask, render_template, request, url_for, redirect, make_response
from flask.ext.login import LoginManager, current_user, login_user, logout_user, login_required
import jinja2

import hashlib
import random
import string

from google.appengine.ext import ndb

app = Flask(__name__)
app.secret_key = 'a6931955dacc453cae352b730334ea9bdab47fce943c5bca'

class User(ndb.Model):
    name = ndb.StringProperty()
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    salt = ndb.StringProperty()

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