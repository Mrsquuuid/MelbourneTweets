
import couchdb
import json
import re
import os
from shapely.geometry import Polygon, MultiPolygon, Point
from afinn import Afinn

def mention_time(text, keyword_list, delimiter):
    return sum([1 if token.lower() in keyword_list else 0 for token in re.split(delimiter, text)])

# CouchDB URL
url_connect = "http://admin:A456852s@127.0.0.1:5984"

# Database list
cities = ["sydney", "brisbane", "melbourne", "perth", "adelaide", "canberra"]
db_names = [f"twitter/city/{city}" for city in cities]

# Split delimiter
delimiter = r"[^a-zA-Z0-9\-]"

# affin object
afinn = Afinn()

# Keywards
keywords_list = dict()
for filename in os.listdir():
    if filename.endswith("txt"):
        with open(filename, "r") as file:
            keywords_list[filename.split(".")[0]] = file.read().split()

# Grid
with open("melb.json") as file:
    grid = json.loads(file.read())["features"]
polygons = []
for loc in grid:
    if loc["geometry"]["type"] == "Polygon":
        polygons.append(Polygon(loc["geometry"]['coordinates'][0]))
    else:
        polygons.append(MultiPolygon([Polygon(each[0]) for each in loc["geometry"]['coordinates']]))
area_list = dict()
area_list["SA2_names"] = [loc["properties"]['SA2_NAME16'] for loc in grid]
area_list["SA2_codes_9_digits"] = [loc["properties"]['SA2_MAIN16'] for loc in grid]
area_list["SA2_codes_5_digits"] = [loc["properties"]['SA2_5DIG16'] for loc in grid]
            
if __name__ == "__main__":
    # Connect CouchDB
    couch = couchdb.Server(url_connect)
    
    # Get all database
    for db_name in db_names:
        db = couch[db_name]
        
        # Get all docs
        all_docs = [i for i in db.view('_all_docs', include_docs=True)]
        
        # Get each doc
        count = 1
        length = len(all_docs)
        for each_doc in all_docs:
            this_doc = dict(each_doc.doc)
            
            # Load text info
            if "full_text" in this_doc:
                this_text = this_doc["full_text"]
            elif "text" in this_doc:
                this_text = this_doc["text"]
            else:
                count += 1 
                continue
            
            # Add field: affin
            this_doc["afinn"] = afinn.score(this_text)
            
            # Add field: keywords
            for key in keywords_list:
                mention = mention_time(this_text, keywords_list[key], delimiter)
                this_doc[key] = mention
            
            # Add field: SA2
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
                    
            # Post each dock
            db.save(this_doc)

            # Print log
            print(f"{count}/{length} docs updated in database: {db_name}", end='\r')
            count += 1 
