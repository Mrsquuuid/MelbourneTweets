import couchdb
import json
import re
import os
import sys
from shapely.geometry import Polygon, MultiPolygon, Point
from afinn import Afinn

def mention_time(text, keyword_list, delimiter):
    return sum([1 if token.lower() in keyword_list else 0 for token in re.split(delimiter, text)])

def read_keywords():
    keywords_list = dict()
    for filename in os.listdir():
        if filename.endswith("txt"):
            with open(filename, "r") as file:
                keywords_list[filename.split(".")[0]] = file.read().split()
    return keywords_list

def read_grid():
    with open("sydney.json") as file:
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
    # Check coordinates info
    if this_doc["coordinates"] is None:
        return False
    
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
    return True

# CouchDB
url_connect = "http://admin:A456852s@127.0.0.1:5984"
couch = couchdb.Server(url_connect)

# Database
db_name = "twitter/hist/sydney"
try:
    couch.create(db_name)
except:
    pass
db = couch[db_name]

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
        while line:
            count += 1
            print(f"Now processing {count}th tweet in Sydney on: {year}/{month}/{day}", end="\r")
            line = line.rstrip().rstrip("]},")
            if not line.endswith('"sydney"'):
                line = raw.readline()
                continue
            this_doc = json.loads(line + "}}")["doc"]
            to_save = add_fields(this_doc, afinn, keywords_list, polygons, area_list)
            if to_save:
                del this_doc['_rev']
                db.save(this_doc)
            line = raw.readline()