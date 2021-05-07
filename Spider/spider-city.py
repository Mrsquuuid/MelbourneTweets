import couchdb
import json
import re
import os
import sys
from shapely.geometry import Polygon, MultiPolygon, Point
from afinn import Afinn
from tweepy import OAuthHandler, Cursor, API
from datetime import datetime

def mention_time(text, keyword_list, delimiter):
    return sum([1 if token.lower() in keyword_list else 0 for token in re.split(delimiter, text)])

def read_keywords():
    keywords_list = dict()
    for filename in os.listdir("keywords"):
        if filename.endswith("txt"):
            with open(os.path.join("keywords", filename), "r") as file:
                keywords_list[filename.split(".")[0]] = file.read().split()
    return keywords_list

def read_grid():
    with open("melb.json") as file:
        return json.loads(file.read())["features"]
        
def read_polygons(grid):
    polygons = []
    for loc in grid:
        if loc["geometry"]["type"] == "Polygon":
            polygons.append(Polygon(loc["geometry"]['coordinates'][0]))
        else:
            polygons.append(MultiPolygon([Polygon(each[0]) for each in loc["geometry"]['coordinates']]))
    return polygons

def read_SA2(grid):
    area_list = dict()
    area_list["SA2_names"] = [loc["properties"]['SA2_NAME16'] for loc in grid]
    area_list["SA2_codes_9_digits"] = [loc["properties"]['SA2_MAIN16'] for loc in grid]
    area_list["SA2_codes_5_digits"] = [loc["properties"]['SA2_5DIG16'] for loc in grid]
    return area_list

def add_fields(this_doc, afinn, keywords_list, polygons, area_list):    
    # Load text info
    this_text = None
    if "full_text" in this_doc:
        this_text = this_doc["full_text"]
    elif "text" in this_doc:
        this_text = this_doc["text"]

    # Add field: affin
    this_doc["afinn"] = afinn.score(this_text)

    # Add field: keywords
    for key in keywords_list:
        mention = mention_time(this_text, keywords_list[key], delimiter)
        this_doc[key] = mention

    # Add field: SA2
    # Check coordinates info
    if this_doc["coordinates"] is not None:
        point = Point(this_doc["coordinates"]["coordinates"])
        index = None
        for i, polygon in enumerate(polygons):
            if polygon.contains(point):
                index = i
                break
        for key in area_list:
            if index is not None:
                this_doc[key] = area_list[key][index]
            else:
                this_doc[key] = None
    else:
        for key in area_list:
            this_doc[key] = None

def harvest_tweet(db, city, tweet_rate, max_id=None, since_id=None):
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file_name = f"log/city/twitter-{city}.log"
    with open(file_name, "a") as file:
        file.write("-------------------------------------------\n")
        file.write(f"Twitter harvest for {city} at {time} begins:\n")
        tweets = Cursor(api.search, q="place:%s" % coords[city], max_id=max_id, since_id=since_id, tweet_mode="extended")
        count = 1
        twi_id = None
        for item in tweets.items(tweet_rate):
            twi_id = item.id_str
            json = item._json
            json["_id"] = twi_id
            add_fields(json, afinn, keywords_list, polygons, area_list)
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
        file.write(f"Twitter harvest for {city} ends at {time}!\n")

# Constants
consumer_key = 'g9mb54pHDFzA5aCGPsiM9Vipp'
consumer_secret = 'Uw3Gsd89iuQaYGMR0suuMmai2k2l3pJaHeK7mhmm6eFDm3CVJG'
access_token = '1384114156488458242-YIXcfIljLhlt1lP63jZrvpZxIRY6iE'
access_token_secret = '5M8G2Nb2saJ46Huar40ouG9TuLpf6dwds6wncHzP6KgGk'

coords = {
    "sydney":"0073b76548e5984f",
    "brisbane": "004ec16c62325149",
    "melbourne":"01864a8a64df9dc4",
    "perth": "0118c71c0ed41109",
    "adelaide": "01e8a1a140ccdc5c",
    "canberra": "01e4b0c84959d430"
}

url_connect = "http://admin:A456852s@127.0.0.1:5984"

mango_max = {"selector": {"_id": {"$gt": None}},"fields": ["_id"],"sort": [{ "_id": "desc" }]}
mango_since = {"selector": {"_id": {"$gt": None}},"fields": ["_id"],"sort": [{ "_id": "asc" }]}

tweet_rate = 1000

# Split delimiter
delimiter = r"[^a-zA-Z0-9\-]"

# affin object
afinn = Afinn()

# Keywards
keywords_list = read_keywords()

# Grid
grid = read_grid()
polygons = read_polygons(grid)
area_list = read_SA2(grid)

# Initialize API
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Initialize couchdb
couch = couchdb.Server(url_connect) 

# Harvest tweet
if __name__ == "__main__":
    for city in coords:
        db_name = f"twitter/city/{city}"
        first = False # first harvest
        try: 
            couch.create(db_name)
            first = True
        except:
            pass
        db = couch[db_name]
        if first:
            harvest_tweet(db, city, tweet_rate)
        else:
            max_id = next(db.find(mango_max)).id
            harvest_tweet(db, city, tweet_rate, since_id=int(max_id)+1)