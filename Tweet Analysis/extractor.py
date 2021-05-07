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

# CouchDB URL
url_connect = "http://admin:A456852s@127.0.0.1:5984"

# Database list
cities = ["sydney", "brisbane", "melbourne", "perth", "adelaide", "canberra"]

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
    # Connect CouchDB
    couch = couchdb.Server(url_connect)
    out_db_name = "twitter/current/all"
    try: 
        couch.create(out_db_name)
        out_db = couch[out_db_name]
    except:
        out_db = couch[out_db_name]
    
    # Get all database
    for city in cities:
        db_name = f"twitter/city/{city}"
        db = couch[db_name]
        
        # Get all docs
        all_docs = [i for i in db.view('_all_docs', include_docs=True)]
        
        # Get each doc
        count = 1
        length = len(all_docs)
        for each_doc in all_docs:
            this_doc = dict(each_doc.doc)

            # Extract features
            out = dict()
            out["_id"] = this_doc["_id"]
            add_fields(this_doc, out, afinn, keywords_list, polygons, area_list, city)
            out_db.save(out)

            # Print log
            print(f"{count}/{length} docs processed in database: {db_name}", end='\r')
            count += 1 
