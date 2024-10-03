from flask import Flask, make_response, jsonify, request
import uuid, random

app = Flask(__name__)

businesses = {}

# For creating an example dataset
def generate_dummy_data():
    towns = ["Coleraine", "Banbridge", "Belfast", "Lisburn", "Ballymena",
        "Derry", "Newry", "Enniskillen", "Omagh", "Ballymoney"]
    buisness_dict = {}
    for i in range(100):
        id = str(uuid.uuid1())
        name = "Biz " + str(i)
        town = towns[random.randint(0, len(towns)-1)]
        rating = random.randint(1,5)
        buisness_dict[id] = {
            "name": name,
            "town": town,
            "rating": rating,
            "reviews": {}
        }
    return buisness_dict

# Retrieve request for all businesses
@app.route("/api/v1.0/businesses", methods=["GET"])
def show_all_businesses():
    return make_response( jsonify( businesses ), 200 )

# Retrieve request for specific business
@app.route("/api/v1.0/businesses/<string:id>", methods=["GET"])
def show_one_business(id):
    return make_response(jsonify(businesses[id]), 200)

# Create business request
@app.route("/api/v1.0/businesses", methods=["POST"])
def add_business():
    next_id = str(uuid.uuid1)
    new_business = {
        "name": request.form["name"],
        "town": request.form["town"],
        "rating": request.form["rating"],
        "reviews": []
    }
    businesses[next_id] = new_business
    return make_response(jsonify({next_id: new_business}), 201)

# Update business request
@app.route("/api/v1.0/businesses/<string:id>", methods=["PUT"])
def edit_business(id):
    businesses[id]["name"] = request.form["name"]
    businesses[id]["town"] = request.form["town"]
    businesses[id]["rating"] = request.form["rating"]
    return make_response(jsonify({id: businesses[id]}), 200)

# Delete business request
@app.route("/api/v1.0/businesses/<string:id>", methods=["DELETE"])
def delete_business(id):
    del businesses[id]
    return make_response(jsonify({}), 200)

# Retrieve request for all reviews
@app.route("/api/v1.0/businesses/<string:id>/reviews", methods=["GET"])
def fetch_all_reviews(id):
    return make_response( jsonify(businesses[id]["reviews"]), 200)

# Retrieve request for specific review
@app.route("/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>", 
    methods=["GET"])
def fetch_one_review(b_id, r_id):
    return make_response(jsonify(businesses[b_id]["reviews"][r_id]), 200)

# Create review request
@app.route("/api/v1.0/businesses/<string:b_id>/reviews", methods=["POST"])
def add_new_review(b_id):
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
    businesses[b_id]["reviews"][r_id]["username"] = request.form["username"]
    businesses[b_id]["reviews"][r_id]["comment"] = request.form["comment"]
    businesses[b_id]["reviews"][r_id]["stars"] = request.form["stars"]
    return make_response(jsonify( \
        {r_id: businesses[b_id]["reviews"][r_id]}), 201)

# Delete review request
@app.route("/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>", 
    methods=["DELETE"])
def delete_review(b_id, r_id):
    del businesses[b_id]["reviews"][r_id]
    return make_response(jsonify({}), 200)

if __name__ == "__main__":
    businesses = generate_dummy_data()
    app.run(debug=True)