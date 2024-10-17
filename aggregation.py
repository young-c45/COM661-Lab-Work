from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.bizDB
businesses = db.biz

pipeline = [
    { "$match" : { "town" : "Banbridge"} },
    { "$project" : {"name" : 1, "num_employees" : 1 } }
]

for business in businesses.aggregate(pipeline):
    print( "Name: ", business["name"], 
        "\t| Number of employees: ", str(business['num_employees']) )