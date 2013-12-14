from flask import Flask
from flask.ext.mongoengine import MongoEngine
app = Flask(__name__, static_folder='static', static_url_path='')
app.config.from_object('config')

db = MongoEngine(app)

from app import routes

#def register_blueprints(app):
    ## Prevent circular imports.
    #from routes import mentors
    #app.register_blueprint(mentors)

#register_blueprints(app)