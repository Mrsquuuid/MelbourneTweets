from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
from datetime import datetime
import couchdb
import json
import re
import os
from shapely.geometry import Polygon, MultiPolygon, Point
from afinn import Afinn

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
        this_text = this_doc["extended_tweet"]["full_text"]
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
        point = Point(this_doc["coordinates"])
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

# Constants
tweet_rate = 5000
consumer_key = 'nLhcOA81zYEUEXkN7CtFZLNWa'
consumer_secret = '5OtSKlWDKYhb6lIFKMdWb0ftv96HmthFwXw26wI6JiUuZv9oNI'
access_token = '1380813622163607552-L0TZIjZaoI6QrFXB7XZ5cxbygNm2YZ'
access_token_secret = 'RRZSs9KCKGjlQLoHaJcG7nE9r2CcxW7RodYzOYnOz13o6'

coords = {
    "melbourne":[144.2600, -38.2900, 146.1100, -37.2400],
    "sydney":[150.1500, -34.1000, 151.2000, -33.2100],
    "canberra":[148.136430,-35.744967,150.113969,-34.860708],
    "brisbane":[152.4228, -27.3924, 153.2806, -27.0116],
    "adelaide":[138.3438, -34.5631, 138.3727, -34.5433],
    "perth":[114.872859,-32.410785,116.850398,-31.491430]
 }

# initialize couchdb
url_connect = "http://admin:qwwq1221@127.0.0.1:5984"
couch = couchdb.Server(url_connect)

class TwitterAuthenticator():
  def auth_twitter_app(self):
      auth = OAuthHandler(consumer_key, consumer_secret)
      auth.set_access_token(access_token, access_token_secret)
      return auth

class TwitterStreamer():
  def __init__(self):
      self.twitter_autenticator = TwitterAuthenticator()

  def stream_tweets(self, db, bounding_box):
      listener = TwitterListener(db)
      auth = self.twitter_autenticator.auth_twitter_app()
      
      stream = Stream(auth, listener)
      stream.filter(locations = bounding_box)

class TwitterListener(StreamListener):
  def __init__(self, db):
    self.db = db
  
  i = 0
  def on_data(self, data):
      json_data = json.loads(data);
    
      try:
        out = dict()
        out["_id"] = json_data["id_str"]
        #add_basics(json_data, out, city)
        add_fields(json_data, out, afinn, keywords_list, polygons, area_list, city)
        db.save(out)
        self.i += 1
        return True
      except:
        pass
      if self.i >= tweet_rate:
        return False

if __name__ == '__main__':
  for city in coords:
    db_name = "twitter/current/all"
    first = False # first harvest
    try:
      couch.create(db_name)
      first = True
    except:
      pass
    db = couch[db_name]
    boundingbox = coords[city]
    my_streamer = TwitterStreamer()
    my_streamer.stream_tweets(db, boundingbox)
