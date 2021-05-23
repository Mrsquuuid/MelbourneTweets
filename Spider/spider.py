import couchdb
import json
import re
import os
from shapely.geometry import Polygon, MultiPolygon, Point
from afinn import Afinn
from tweepy import OAuthHandler, Cursor, API
from datetime import datetime

def read_keywords():
    keywords_list = dict()
    for filename in os.listdir("keywords"):
        if filename.endswith("txt"):
            with open(os.path.join("keywords", filename), "r") as file:
                keywords_list[filename.split(".")[0]] = file.read().split()
    return keywords_list

def read_grid():
    grid = dict()
    with open("grid/melb.json") as file:
        grid["melbourne"] = json.loads(file.read())["features"]
    with open("grid/sydney.json") as file:
        grid["sydney"] = json.loads(file.read())["features"]
    return grid
        
def read_polygons(grid):
    polygons = dict()
    for city in grid:
        sub_polygons = []
        for loc in grid[city]:
            if loc["geometry"]["type"] == "Polygon":
                sub_polygons.append(Polygon(loc["geometry"]['coordinates'][0]))
            else:
                sub_polygons.append(MultiPolygon([Polygon(each[0]) for each in loc["geometry"]['coordinates']]))
        polygons[city] = sub_polygons
    return polygons

def read_SA2(grid):
    area_list = dict()
    for city in grid:
        sub_area_list = {}
        sub_area_list["SA2_names"] = [loc["properties"]['SA2_NAME16'] for loc in grid[city]]
        sub_area_list["SA2_codes_9_digits"] = [loc["properties"]['SA2_MAIN16'] for loc in grid[city]]
        sub_area_list["SA2_codes_5_digits"] = [loc["properties"]['SA2_5DIG16'] for loc in grid[city]]
        area_list[city] = sub_area_list
    return area_list

def add_basics(this_doc, out, city):
    this_text = None
    try:
        this_text = this_doc["full_text"]
    except:
        this_text = this_doc["text"]
    out["text"] = this_text
    out["lang"] = this_doc["lang"]
    out["location"] = city
    return this_text

def add_time(this_doc, out):
    this_time = this_doc["created_at"].split()
    out["year"] = this_time[5]
    out["month"] = this_time[1]
    out["day"] = this_time[2]

def mention_time(word_list, keyword_list):
    return sum([1 if token.lower() in keyword_list else 0 for token in word_list])   

def add_SA2(this_doc, out, polygons, area_list):
    # Add default value
    for key in area_list["sydney"]:
        out[key] = None
    # Check coordinates info
    city = out["location"]
    if city in area_list and this_doc["coordinates"] is not None:
        point = Point(this_doc["coordinates"]["coordinates"])
        index = None
        for i, polygon in enumerate(polygons[city]):
            if polygon.contains(point):
                index = i
                break
        if index is not None:
            for key in area_list[city]:
                out[key] = area_list[city][key][index]

def add_fields(this_doc, out, afinn, keywords_list, polygons, area_list, city): 
    # Load and add field: text, language, location
    this_text = add_basics(this_doc, out, city)

    # Add field: time
    add_time(this_doc, out)

    # Add field: affin
    out["afinn"] = afinn.score(this_text)

    # Add field: keywords
    for key in keywords_list:
        out[key] = mention_time(re.split(delimiter, this_text), keywords_list[key])

    # Add field: SA2
    add_SA2(this_doc, out, polygons, area_list)

def harvest_tweet(db, city, tweet_rate, max_id=None, since_id=None):
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file_name = f"log/twitter-current-all.log"
    with open(file_name, "a") as file:
        file.write(f"Twitter harvest for {city} at begins at: {time}\n")
        tweets = Cursor(api.search, q="place:%s" % coords[city], max_id=max_id, since_id=since_id, tweet_mode="extended")
        count = 1
        for item in tweets.items(tweet_rate):
            out = dict()
            out["_id"] = item.id_str
            add_fields(item._json, out, afinn, keywords_list, polygons, area_list, city)
            db.save(out)
            count += 1
        file.write(f"Number of tweets saved: {count-1}\n")
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file.write(f"Twitter harvest for {city} ends at: {time}\n")
        file.write("-------------------------------------------\n")

# Constants
# Twitter authentication
consumer_key = 'g9mb54pHDFzA5aCGPsiM9Vipp'
consumer_secret = 'Uw3Gsd89iuQaYGMR0suuMmai2k2l3pJaHeK7mhmm6eFDm3CVJG'
access_token = '1384114156488458242-YIXcfIljLhlt1lP63jZrvpZxIRY6iE'
access_token_secret = '5M8G2Nb2saJ46Huar40ouG9TuLpf6dwds6wncHzP6KgGk'

# City information
coords = {
    "sydney":"0073b76548e5984f",
    "brisbane": "004ec16c62325149",
    "melbourne":"01864a8a64df9dc4",
    "perth": "0118c71c0ed41109",
    "adelaide": "01e8a1a140ccdc5c",
    "canberra": "01e4b0c84959d430"
}

# CouchDB URL
url_connect = "http://admin:A456852s@127.0.0.1:5984"

# Mango query
mango_max = {
    "selector": {"_id": {"$gt": None}, "location": None},
    "fields": ["_id"],
    "sort": [{ "_id": "desc" }]
}

# Harvest number
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
    # Select database
    db_name = "twitter/current/all"
    first = True
    try: 
        couch.create(db_name)
        db = couch[db_name]
    except:
        db = couch[db_name]
        first = False
    for city in coords:
        if first:
            harvest_tweet(db, city, tweet_rate)
        else:
            mango_max["selector"]["location"] = city
            max_id = next(db.find(mango_max)).id
            harvest_tweet(db, city, tweet_rate, since_id=int(max_id)+1)