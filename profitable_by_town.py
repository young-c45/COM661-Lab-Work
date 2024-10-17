from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.bizDB
businesses = db.biz

bizCount = businesses.aggregate([
    { "$group": {
        "_id": "$town",
        "count": { "$sum": 1 }
    }}
])

mostProfit = businesses.aggregate([
    { "$project": {
        "name": 1,
        "town": 1,
        "profit": 1,
        "_id": 0
    }},
    { "$unwind": "$profit" },
    { "$group": {
        "_id": { "year": "$profit.year", "town": "$town"},
        "topBiz": { "$top": { 
            "output": "$name",
            "sortBy": { "profit.gross": -1 }
        }}
    }},
    { "$sort": { "_id.year": -1 } },
    { "$group": {
        "_id": "$_id.town",
        "topBiz": { "$push": {
            "year": "$_id.year",
            "name": "$topBiz"
        }}
    }},
    { "$sort": { "_id": 1 } }
])

count = {}

for town in bizCount:
    count[town["_id"]] = town["count"]

for town in mostProfit:
    print("\nTown name:\t", town["_id"],
        "\nNum of buisness:", count[town["_id"]],
        "\nTop buisness:")
    for buisness in town["topBiz"]:
        print("\t\t",buisness["year"], " - ", buisness["name"])