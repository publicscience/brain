from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__, static_folder='static', static_url_path='')

# Load config.
app.config.from_object('config')

# Setup the database.
db = MongoEngine(app)

from app import routes, brain
import schedule

"""
Fetch tweets and memorize and process them
every hour.
"""
schedule.every().hour.do(brain.ponder)