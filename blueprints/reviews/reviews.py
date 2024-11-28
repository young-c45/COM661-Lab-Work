from flask import Blueprint, request, make_response, jsonify
from decorators import jwt_required, admin_required
from bson import ObjectId
import globals

reviews_bp = Blueprint("reviews_bp", __name__)

businesses = globals.db.biz

# Create review request
@reviews_bp.route("/api/v1.0/businesses/<string:b_id>/reviews", 
    methods=["POST"])
#@jwt_required
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
@reviews_bp.route("/api/v1.0/businesses/<string:b_id>/reviews", methods=["GET"])
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
@reviews_bp.route("/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>", 
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
@reviews_bp.route("/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>", 
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
@reviews_bp.route("/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>", 
    methods=["DELETE"])
@jwt_required
@admin_required
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
