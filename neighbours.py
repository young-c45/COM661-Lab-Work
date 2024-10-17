from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.bizDB
businesses = db.biz

for business in businesses.aggregate( [ { "$sample" : { "size": 1 } } ] ):
    print("Random business is " + business["name"] + " from " + business["town"])

    for neighbour in businesses.aggregate( [
                { "$geoNear" : 
                    { "near" : { "type" : "Point", 
                                "coordinates" : business["location"]["coordinates"] },
                      "maxDistance": 50000,
                      "minDistance" : 1,
                      "distanceField" : "distance",
                      "spherical" : True
                    }
                },
                { "$match" : { "town" : { "$ne": business["town"] } } },
                { "$project" : { "name" : 1, "town" : 1, "distance" : 1 } },
                { "$limit" : 10 }
            ]):
        distance_km = str(round(neighbour["distance"] / 1000))
        print(neighbour["name"] + " from " + neighbour["town"] + " is at a distance of " + distance_km + " km" )    
