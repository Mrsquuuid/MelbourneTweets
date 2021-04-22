from tweepy import OAuthHandler, Cursor, API
from datetime import datetime
import couchdb, requests, time

# Constants
consumer_key = 'g9mb54pHDFzA5aCGPsiM9Vipp'
consumer_secret = 'Uw3Gsd89iuQaYGMR0suuMmai2k2l3pJaHeK7mhmm6eFDm3CVJG'
access_token = '1384114156488458242-YIXcfIljLhlt1lP63jZrvpZxIRY6iE'
access_token_secret = '5M8G2Nb2saJ46Huar40ouG9TuLpf6dwds6wncHzP6KgGk'

coords = {
    "sydney":"0073b76548e5984f",
    "brisbane": "004ec16c62325149"
}

url_connect = "http://admin:A456852s@127.0.0.1:5984"
url_dbs = "http://admin:A456852s@127.0.0.1:5984/_all_dbs"

that_day = "2021_04_22"

mango_max = {"selector": {"_id": {"$gt": None}},"fields": ["_id"],"sort": [{ "_id": "desc" }]}
mango_since = {"selector": {"_id": {"$gt": None}},"fields": ["_id"],"sort": [{ "_id": "asc" }]}

tweet_rate = 100

# Initialize API
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Initialize couchdb
couch = couchdb.Server(url_connect) 

# Get all existing dbs
resp = requests.get(url_dbs)
dbs = [db.strip('[]"\n') for db in resp.text.split(",")]

def harvest_tweet(db, city, that_day, tweet_rate, max_id=None, since_id=None):
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file_name = f"log/city/twitter-{city}-{that_day}.log"
    with open(file_name, "a") as file:
        file.write("-------------------------------------------\n")
        file.write(f"Historical twitter harvest for {city} at {time} begins:\n")
        tweets = Cursor(api.search, q="place:%s" % coords[city], max_id=max_id, since_id=since_id)
        count = 1
        for item in tweets.items(tweet_rate):
            max_id = item.id_str
            json = item._json
            json["_id"] = max_id
            db.save(json)
            if count == 1:
                file.write(f"Starting tweet ID: {max_id}\n")
            if count % 10 == 0:
                file.write(".")
            if count % 100 == 0:
                file.write(f"\n{count}/{tweet_rate} tweet saved succesfully!\n")
            count += 1
        file.write(f"In total {count-1} tweets saved!\n")
        file.write(f"Ending tweet ID: {max_id}\n")
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file.write(f"Historical twitter harvest for {city} ends at {time}!\n")

# Harvest tweet
if __name__ == "__main__":
    for city in coords:
        db_name = f"twitter/city/{city}/{that_day}"
        db = couch[db_name]
        since_id = next(db.find(mango_since)).id
        harvest_tweet(db, city, that_day, tweet_rate, max_id=int(since_id)-1)