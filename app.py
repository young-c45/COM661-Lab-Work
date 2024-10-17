from flask import Flask, make_response, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.bizDB
businesses = db.biz

def jwt_required(func):
    @wraps(func)
    def jwt_required_wrapper(*args, **kwargs):
        if "x-access-token" in request.headers:
            token = request.headers['x-access-token']
        else:
            return make_response(jsonify({"message": "Token is missing"}), 401)
        
        try:
            data = jwt.decode(
                token,
                app.config['SECRET_KEY'],
                algorithms="HS256"
            )
        except:
            return make_response(jsonify({"message": "Token is invalid"}), 401)
        
        return func(*args, **kwargs)
    return jwt_required_wrapper

# Create business request
@app.route("/api/v1.0/businesses", methods=["POST"])
@jwt_required
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

# Update business request
@app.route("/api/v1.0/businesses/<string:id>", methods=["PUT"])
@jwt_required
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
@jwt_required
def delete_business(id):
    try:
        result = businesses.delete_one({"_id": ObjectId(id)})
    except:
        return make_response(jsonify({"error": "Invalid business ID"}), 404)
    
    if result.deleted_count == 1:
        return make_response(jsonify({}), 200)
    else:
        return make_response(jsonify({"error": "Invalid business ID"}), 404)

# Create review request
@app.route("/api/v1.0/businesses/<string:b_id>/reviews", methods=["POST"])
@jwt_required
def add_new_review(b_id):
    if "username" not in request.form \
    or "comment" not in request.form \
    or "stars" not in  request.form:
        return make_response(jsonify({"error": "Missing form data"}), 404)
    
    try:
        b_idObject = ObjectId(b_id)
    except:
        return make_response(jsonify({"error": "Invalid business ID"}), 404)

    new_review = {
        "_id": ObjectId(),
        "username": request.form["username"],
        "comment": request.form["comment"],
        "stars": request.form["stars"]
    }

    result = businesses.update_one({"_id": b_idObject}, \
        {"$push": {"reviews": new_review}})
    if result.matched_count == 1:
        new_review_link = "http://localhost:5000/api/v1.0/businesses/" \
            + b_id + "/reviews/" + str(new_review['_id'])
        return make_response(jsonify({"url": new_review_link}), 201)
    else:
        return make_response(jsonify({"error": "Invalid business ID"}), 404)

# Retrieve request for all reviews
@app.route("/api/v1.0/businesses/<string:b_id>/reviews", methods=["GET"])
def fetch_all_reviews(b_id):
    try:
        business = businesses.find_one({"_id": ObjectId(b_id)}, \
            {"reviews": 1, "_id": 0})
    except:
        return make_response(jsonify({"error": "Invalid business ID"}), 404)
    
    if business is None:
        return make_response(jsonify({"error": "Invalid business ID"}), 404)
    
    data_to_return = []
    for review in business["reviews"]:
        review["_id"] = str(review["_id"])
        data_to_return.append(review)

    return make_response( jsonify( data_to_return ), 200 )

# Retrieve request for specific review
@app.route("/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>", 
    methods=["GET"])
def fetch_one_review(b_id, r_id):
    try:
        r_idObject = ObjectId(r_id)
    except:
        return make_response(jsonify( \
            {"error": "Invalid business or review ID"}), 404)
    
    business = businesses.find_one(
        {"reviews._id": r_idObject},
        {"_id": 0, "reviews.$": 1}
    )

    if business is None:
        return make_response(jsonify( \
            {"error": "Invalid business or review ID"}), 404)
    
    review = business['reviews'][0]
    review['_id'] = str(review['_id'])
    
    return make_response(jsonify(review), 200)

# Update review request
@app.route("/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>", 
    methods=["PUT"])
@jwt_required
def edit_review(b_id, r_id):
    if "username" not in request.form \
    or "comment" not in request.form \
    or "stars" not in  request.form:
        return make_response(jsonify({"error": "Missing form data"}), 404)
    
    try:
        r_idObject = ObjectId(r_id)
    except:
        return make_response(jsonify( \
            {"error": "Invalid business or review ID"}), 404)
    
    edited_review = {
        "reviews.$.username": request.form["username"],
        "reviews.$.comment": request.form["comment"],
        "reviews.$.stars": request.form["stars"]
    }

    result = businesses.update_one(
        {"reviews._id": r_idObject},
        {"$set": edited_review}
    )

    if result.matched_count == 1:
        edit_review_link = "http://localhost:5000/api/v1.0/businesses/" \
            + b_id + "/reviews/" + r_id
        return make_response(jsonify({"url": edit_review_link}), 200)
    else:
        return make_response(jsonify( \
            {"error": "Invalid business or review ID"}), 404)

# Delete review request
@app.route("/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>", 
    methods=["DELETE"])
@jwt_required
def delete_review(b_id, r_id):
    try:
        b_idObject = ObjectId(b_id)
    except:
        return make_response(jsonify({"error": "Invalid business ID"}), 404)
    
    try:
        r_idObject = ObjectId(r_id)
    except:
        return make_response(jsonify( \
            {"error": "Invalid review ID"}), 404)
    
    result = businesses.update_one(
        {"_id": b_idObject, "reviews._id": r_idObject},
        {"$pull": {"reviews": {"_id": r_idObject}}}
    )

    if result.matched_count == 1:
        return make_response(jsonify({}), 204)
    else:
        return make_response(jsonify( \
            {"error": "Invalid business or review ID"}), 404)

@app.route("/api/v1.0/login", methods=['GET'])
def login():
    auth = request.authorization
    if auth and auth.password == "password":
        token = jwt.encode({
            "user": auth.username,
            "exp": datetime.datetime.now(datetime.UTC) +
                datetime.timedelta(minutes=30)},
            app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return make_response(jsonify({"token": token}), 200)
    return make_response("Could not verify", 401,\
        {"WWW-Authenticate": 'Basic realm = "Login required"'})

if __name__ == "__main__":
    app.run(debug=True)