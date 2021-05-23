import couchdb
import json
import re
import os
import sys
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
        sub_area_list = dict()
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
    time_list = this_time[3].split(":")
    out["time"] = time_list
    out["zone"] = this_time[4]

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
        return True
    return False

def add_fields(this_doc, out, afinn, keywords_list, polygons, area_list, city): 
    # Initialize output
    to_save = [False, False]

    # Load and add field: text, language, location
    this_text = add_basics(this_doc, out, city)

    # Add field: time
    add_time(this_doc, out)

    # Add field: affin
    out["afinn"] = afinn.score(this_text)

    # Add field: keywords
    key_word_count = 0 
    for key in keywords_list:
        out[key] = mention_time(re.split(delimiter, this_text), keywords_list[key])
        key_word_count += out[key]
    if key_word_count > 0:
        to_save[1] = True

    # Add field: SA2
    to_save[0] = add_SA2(this_doc, out, polygons, area_list)

    # Whether save or not
    return to_save[0], to_save[1]

# CouchDB
url_connect = "http://admin:A456852s@127.0.0.1:5984"
couch = couchdb.Server(url_connect)

# Database
city = sys.argv[4]
db_name_geo = f"twitter/hist/{city}/geo"
db_name_relative = f"twitter/hist/{city}/relative"
try:
    couch.create(db_name_geo)
except:
    pass
try:
    couch.create(db_name_relative)
except:
    pass
db_geo = couch[db_name_geo]
db_relative = couch[db_name_relative]

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

if __name__ == "__main__":
    # Load command line args
    year = sys.argv[1]
    month = sys.argv[2]
    day = sys.argv[3]

    # Process each line
    with open(f"temp/twitter.json", "r") as raw:
        line = raw.readline()
        count = 0
        count_geo = 0
        count_relative = 0
        while line:
            count += 1
            print(f"Now processing {count}th tweet in Sydney on: {year}/{month}/{day}", end="\r")
            line = line.rstrip().rstrip("]},")
            try:
                this_doc = json.loads(line + "}}")["doc"]
            except:
                line = raw.readline()
                continue
            out = dict()
            out["_id"] = this_doc["_id"]
            to_save_geo, to_save_relative = add_fields(this_doc, out, afinn, keywords_list, polygons, area_list, city)
            if to_save_geo:
                count_geo += 1
                db_geo.save(out)
            if to_save_relative:
                count_relative += 1
                db_relative.save(out)
            line = raw.readline()
        print(f"Number of tweets in Sydney added to {db_name_geo}: {count_geo}")
        print(f"Number of tweets in Sydney added to {db_name_relative}: {count_relative}")