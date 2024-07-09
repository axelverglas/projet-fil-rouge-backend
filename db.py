from flask_pymongo import PyMongo
import certifi

mongo = PyMongo(tlsCAFile=certifi.where())

def get_db():
    return mongo.db