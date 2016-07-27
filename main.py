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

# Login management
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def create_user(name, username, password):
	# Generate random salt
	salt = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for i in range(0, 15))

	# Generate password hash
	m = hashlib.sha512()
	m.update(salt)
	m.update(password)
	password_hash = m.hexdigest()

	return User(name=name, username=username, password=password_hash, salt=salt)

@login_manager.user_loader
def load_user(userid):
	return User.query().filter(User.username == userid).get()

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')

	elif request.method == 'POST':
		user = load_user(request.form['username'])

		if user:
			if user.check_password_hash(request.form['password']):
				login_user(user, remember=True)
				return redirect(url_for('home'))

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'GET':
		return render_template('register.html')

	elif request.method == 'POST':
		# Check to see if username is taken
		user = User.query(User.username == request.form['username']).get()

		if user:
			return render_template('register.html', message='Username taken')

		name = request.form['fullname']
		username = request.form['username']
		password = request.form['password']
		new_user = create_user(name, username, password)
		new_user.put()

		return render_template('login.html', message='Thank you for creating an account! Please log in with your credentials.')