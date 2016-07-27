from flask import Flask, render_template, request, url_for, redirect, make_response
from flask.ext.login import LoginManager, current_user, login_user, logout_user, login_required
import jinja2

import hashlib
import random
import string

from google.appengine.ext import ndb

app = Flask(__name__)
app.secret_key = 'a6931955dacc453cae352b730334ea9bdab47fce943c5bca'