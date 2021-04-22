from tweepy import OAuthHandler, Cursor, API
from datetime import datetime
import couchdb, requests

# Constants
consumer_key = 'g9mb54pHDFzA5aCGPsiM9Vipp'
consumer_secret = 'Uw3Gsd89iuQaYGMR0suuMmai2k2l3pJaHeK7mhmm6eFDm3CVJG'
access_token = '1384114156488458242-YIXcfIljLhlt1lP63jZrvpZxIRY6iE'
access_token_secret = '5M8G2Nb2saJ46Huar40ouG9TuLpf6dwds6wncHzP6KgGk'

coords = {
    "melbourne":"-37.8300,144.9564,50km",
    "sydney":"-33.8688,151.2093,50km",
    "brisbane": "-27.4701,153.0211,50km",
    "perth": "-31.9523,115.8613,50km",
    "adelaide": "-34.9212,138.5995,50km",
    "canberra": "-35.2820,149.1290,50km",
    "darwin": "-12.4628,130.8417.50km"
}

url_connect = "http://admin:A456852s@127.0.0.1:5984"
url_dbs = "http://admin:A456852s@127.0.0.1:5984/_all_dbs"

today = datetime.now().strftime("%Y_%m_%d")

mango_max = {"selector": {"_id": {"$gt": None}},"fields": ["_id"],"sort": [{ "_id": "desc" }]}
mango_since = {"selector": {"_id": {"$gt": None}},"fields": ["_id"],"sort": [{ "_id": "asc" }]}

tweet_rate = 1000

# Initialize API
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Initialize couchdb
couch = couchdb.Server(url_connect) 

# Get all existing dbs
resp = requests.get(url_dbs)
dbs = [db.strip('[]"\n') for db in resp.text.split(",")]

def harvest_tweet(db, city, tweet_rate, max_id=None, since_id=None):
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    today = datetime.now().strftime("%Y_%m_%d")
    file_name = f"twitter_{city}_{today}.log"
    with open(file_name, "a") as file:
        file.write("-------------------------------------------\n")
        file.write(f"Twitter harvest for {city} at {time} begins:\n")
        tweets = Cursor(api.search, geocode=coords[city], max_id=max_id, since_id=since_id)
        count = 1
        for item in tweets.items(tweet_rate):
            max_id = item.id_str
            json = item._json
            json["_id"] = max_id
            db.save(json)
            if count % 10 == 0:
                file.write(".")
            if count % 100 == 0:
                file.write(f"\n{count}/{tweet_rate} tweet saved succesfully!\n")
            count += 1
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file.write(f"Twitter harvest for {city} ends at {time}!\n")

# Harvest tweet
if __name__ == "__main__":
    for city in coords:
        db_name = f"twitter_{city}_{today}"
        first = False # first harvest today
        if db_name not in dbs:
            couch.create(db_name)
            first = True
        db = couch[db_name]
        if first:
            harvest_tweet(db, city, tweet_rate)
        else:
            max_id = next(db.find(mango_max)).id
            since_id = next(db.find(mango_max)).id
            harvest_tweet(db, city, tweet_rate, since_id=max_id+1)
