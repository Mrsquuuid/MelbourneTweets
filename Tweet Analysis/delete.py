import couchdb

# CouchDB URL
url_connect = "http://admin:A456852s@127.0.0.1:5984"

# Database list
coords = None
with open("area_code.json") as file:
    coords = json.loads(file.read())
db_names = []
for SA4 in coords:
        SA4_dict = coords[SA4]
        for SA3 in SA4_dict:
            SA3_dict = SA4_dict[SA3]
            for SA2 in SA3_dict:
                area_code = SA3_dict[SA2]
                db_names.append(f"twitter/{SA4}/{SA3}/{SA2}")
            
if __name__ == "__main__":
    # Connect CouchDB
    couch = couchdb.Server(url_connect)
    
    # Get all database
    for db_name in db_names:
        couch.delete(db_name)