from google.appengine.api import users
from google.appengine.ext import db

class Entry(db.Model):
	#author = None # Foreign key to users where users are google users rather than django users
	created_date = db.DateTimeProperty(auto_now_add=True)
	edited_date = db.DateTimeProperty(auto_now=True)
	title = db.StringProperty()
	content = db.TextProperty()
	#topics = None # list of words
	
	