import pymongo
import json
# Creating a pymongo client instance

db_url = "mongodb://pc77:Parul123@ds157819.mlab.com:57819/crawler_data?retryWrites=false"
client = pymongo.MongoClient(db_url)
db = client["crawler_data"]
collection = db["apidata"]

with open('data.json', 'r') as f:
    file_data = json.load(f)
try:
    collection.insert_one(file_data)
except pymongo.errors.ServerSelectionTimeoutError as e:
    print("Couldn't connect to the Database .. ", e)
client.close()
