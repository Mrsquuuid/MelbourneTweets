from tweepy import OAuthHandler, Cursor, API
from datetime import datetime
import couchdb, json

# Constants
consumer_key = 'g9mb54pHDFzA5aCGPsiM9Vipp'
consumer_secret = 'Uw3Gsd89iuQaYGMR0suuMmai2k2l3pJaHeK7mhmm6eFDm3CVJG'
access_token = '1384114156488458242-YIXcfIljLhlt1lP63jZrvpZxIRY6iE'
access_token_secret = '5M8G2Nb2saJ46Huar40ouG9TuLpf6dwds6wncHzP6KgGk'

coords = None
with open("area_code.json") as file:
    coords = json.loads(file.read())

url_connect = "http://admin:A456852s@127.0.0.1:5984"

mango_max = {"selector": {"_id": {"$gt": None}},"fields": ["_id"],"sort": [{ "_id": "desc" }]}
mango_since = {"selector": {"_id": {"$gt": None}},"fields": ["_id"],"sort": [{ "_id": "asc" }]}

tweet_rate = 1000

# Initialize API
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Initialize couchdb
couch = couchdb.Server(url_connect) 

def harvest_tweet(db, area_code, SA, weet_rate, max_id=None, since_id=None):
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file_name = f"log/suburb/twitter-{SA[0]}-{SA[1]}-{SA[2]}.log"
    with open(file_name, "a") as file:
        file.write("-------------------------------------------\n")
        file.write(f"Twitter harvest for {SA[0]}/{SA[1]}/{SA[2]} at {time} begins:\n")
        tweets = Cursor(api.search, q="place:%s" % area_code, max_id=max_id, since_id=since_id)
        count = 1
        twi_id = None
        for item in tweets.items(tweet_rate):
            twi_id = item.id_str
            json = item._json
            json["_id"] = twi_id
            db.save(json)
            if count == 1:
                file.write(f"Starting tweet ID: {twi_id}\n")
            if count % 10 == 0:
                file.write(".")
            if count % 100 == 0:
                file.write(f"\n{count}/{tweet_rate} tweet saved succesfully!\n")
            count += 1
        file.write(f"In total {count-1} tweets saved!\n")
        file.write(f"Ending tweet ID: {twi_id}\n")
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file.write(f"Twitter harvest for {SA[0]}/{SA[1]}/{SA[2]} ends at {time}!\n")

# Harvest tweet
if __name__ == "__main__":
    for SA4 in coords:
        SA4_dict = coords[SA4]
        for SA3 in SA4_dict:
            SA3_dict = SA4_dict[SA3]
            for SA2 in SA3_dict:
                area_code = SA3_dict[SA2]
                db_name = f"twitter/{SA4}/{SA3}/{SA2}"
                first = False # first harvest
                try:
                    couch.create(db_name)
                    first = True
                except:
                    pass
                db = couch[db_name]
                if first:
                    harvest_tweet(db, area_code, (SA4, SA3, SA2), tweet_rate)
                else:
                    try:
                        max_id = next(db.find(mango_max)).id
                        harvest_tweet(db, area_code, (SA4, SA3, SA2), tweet_rate, since_id=int(max_id)+1)
                    except:
                        harvest_tweet(db, area_code, (SA4, SA3, SA2), tweet_rate)
