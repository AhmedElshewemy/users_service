from pymongo import MongoClient

# client = MongoClient('mongodb://localhost:27017/') 

client = MongoClient("mongodb://mongodb:27017/")
db = client["my_database"]
users = db['users']
