""" from flask_sqlalchemy import SQLAlchemy
#file that creates instance of SQLAlchemy
db = SQLAlchemy() """
from flask_mongoengine import MongoEngine
db=MongoEngine()