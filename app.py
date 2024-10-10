from flask import Flask, make_response, jsonify, request
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.bizDB
businesses = db.biz

# Retrieve request for all businesses
@app.route("/api/v1.0/businesses", methods=["GET"])
def show_all_businesses():
    page_num, page_size = 1, 10
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
        
    page_start = (page_size * (page_num - 1))

    data_to_return = []
    for business in businesses.find().skip(page_start).limit(page_size):
        # Converts ids to strings
        business['_id'] = str(business['_id'])
        for review in business['reviews']:
            review['_id'] = str(review['_id'])
        data_to_return.append(business)

    return make_response( jsonify( data_to_return ), 200 )

# Retrieve request for specific business
@app.route("/api/v1.0/businesses/<string:id>", methods=["GET"])
def show_one_business(id):
    try:
        business = businesses.find_one({'_id':ObjectId(id)})
    except:
        return make_response(jsonify({"error": "Invalid business ID"}), 404)

    if business is not None:
        # Converts ids to strings
        business['_id'] = str(business['_id'])
        for review in business['reviews']:
            review['_id'] = str(review['_id'])
        return make_response(jsonify(business), 200)
    else:
        return make_response(jsonify({"error": "Invalid business ID"}), 404)

# Create business request
@app.route("/api/v1.0/businesses", methods=["POST"])
def add_business():
    if "name" not in request.form \
    or "town" not in request.form \
    or "rating" not in  request.form:
        return make_response(jsonify({"error": "Missing form data"}), 404)

    new_business = {
        "name": request.form["name"],
        "town": request.form["town"],
        "rating": request.form["rating"],
        "reviews": []
    }
    new_business_id = businesses.insert_one(new_business)
    new_business_link = "http://localhost:5000/api/v1.0/businesses/" \
        + str(new_business_id.inserted_id)
    return make_response(jsonify({"url": new_business_link}), 201)

# Update business request
@app.route("/api/v1.0/businesses/<string:id>", methods=["PUT"])
def edit_business(id):
    if "name" not in request.form \
    or "town" not in request.form \
    or "rating" not in  request.form:
        return make_response(jsonify({"error": "Missing form data"}), 404)
    
    try:
        idObject = ObjectId(id)
    except:
        return make_response(jsonify({"error": "Invalid business ID"}), 404)
    
    result = businesses.update_one({"_id": idObject}, {"$set": {
        "name": request.form["name"],
        "town": request.form["town"],
        "rating": request.form["rating"]
    }})

    if result.matched_count == 1:
        edited_buisness_link = "http://localhost:5000/api/v1.0/businesses/" \
        + id
        return make_response(jsonify({"url": edited_buisness_link}), 200)
    else:
        return make_response(jsonify({"error": "Invalid business ID"}), 404)

# Delete business request
@app.route("/api/v1.0/businesses/<string:id>", methods=["DELETE"])
def delete_business(id):
    try:
        result = businesses.delete_one({"_id": ObjectId(id)})
    except:
        return make_response(jsonify({"error": "Invalid business ID"}), 404)
    
    if result.deleted_count == 1:
        return make_response(jsonify({}), 200)
    else:
        return make_response(jsonify({"error": "Invalid business ID"}), 404)


"""

# Retrieve request for all reviews
@app.route("/api/v1.0/businesses/<string:id>/reviews", methods=["GET"])
def fetch_all_reviews(id):
    if id not in businesses:
        return make_response(jsonify({"error": "Invalid business ID"}), 404)
    
    page_num, page_size = 1, 10
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
        
    page_start = (page_size * (page_num - 1))
    reviews_list = [{k : v} for k,v in businesses[id]["reviews"].items()]
    data_to_return = reviews_list[page_start : page_start+page_size]

    return make_response( jsonify( data_to_return ), 200 )

# Retrieve request for specific review
@app.route("/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>", 
    methods=["GET"])
def fetch_one_review(b_id, r_id):
    if b_id not in businesses:
        return make_response(jsonify({"error": "Invalid business ID"}), 404)
    elif r_id not in businesses[b_id]["reviews"]:
        return make_response(jsonify({"error": "Invalid review ID"}), 404)
    
    return make_response(jsonify(businesses[b_id]["reviews"][r_id]), 200)

# Create review request
@app.route("/api/v1.0/businesses/<string:b_id>/reviews", methods=["POST"])
def add_new_review(b_id):
    if b_id not in businesses:
        return make_response(jsonify({"error": "Invalid business ID"}), 404)
    elif "username" not in request.form \
    or "comment" not in request.form \
    or "stars" not in  request.form:
        return make_response(jsonify({"error": "Missing form data"}), 404)
    
    new_review_id = str(uuid.uuid1())
    new_review = {
        "username": request.form["username"],
        "comment": request.form["comment"],
        "stars": request.form["stars"]
    }
    businesses[b_id]["reviews"][new_review_id] = new_review
    return make_response(jsonify({new_review_id: new_review}), 201)

# Update review request
@app.route("/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>", 
    methods=["PUT"])
def edit_review(b_id, r_id):
    if b_id not in businesses:
        return make_response(jsonify({"error": "Invalid business ID"}), 404)
    elif r_id not in businesses[b_id]["reviews"]:
        return make_response(jsonify({"error": "Invalid review ID"}), 404)

    is_edited = False
    for key, value in request.form.items():
        if key in businesses[b_id]["reviews"][r_id]:
            is_edited = True
            businesses[b_id]["reviews"][r_id][key] = value
    if is_edited:
        return make_response(jsonify( \
        {r_id: businesses[b_id]["reviews"][r_id]}), 201)
    else:
        return make_response(jsonify({"error": "Missing form data"}), 404)

# Delete review request
@app.route("/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>", 
    methods=["DELETE"])
def delete_review(b_id, r_id):
    if b_id not in businesses:
        return make_response(jsonify({"error": "Invalid business ID"}), 404)
    elif r_id not in businesses[b_id]["reviews"]:
        return make_response(jsonify({"error": "Invalid review ID"}), 404)
    
    del businesses[b_id]["reviews"][r_id]
    return make_response(jsonify({}), 200)
"""


if __name__ == "__main__":
    app.run(debug=True)