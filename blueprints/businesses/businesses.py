from flask import Blueprint, request, make_response, jsonify
from decorators import jwt_required, admin_required
from bson import ObjectId
import globals

businesses_bp = Blueprint("buisnesses_bp", __name__)

businesses = globals.db.biz

# Create business request
@businesses_bp.route("/api/v1.0/businesses", methods=["POST"])
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
@businesses_bp.route("/api/v1.0/businesses", methods=["GET"])
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
@businesses_bp.route("/api/v1.0/businesses/<string:id>", methods=["GET"])
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
@businesses_bp.route("/api/v1.0/businesses/<string:id>", methods=["PUT"])
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
@businesses_bp.route("/api/v1.0/businesses/<string:id>", methods=["DELETE"])
@jwt_required
@admin_required
def delete_business(id):
    try:
        result = businesses.delete_one({"_id": ObjectId(id)})
    except:
        return make_response(jsonify({"error": "Invalid business ID"}), 404)
    
    if result.deleted_count == 1:
        return make_response(jsonify({}), 204)
    else:
        return make_response(jsonify({"error": "Invalid business ID"}), 404)
