"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints.
"""
import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users, People, Planets, Favorites  

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL", "sqlite:///test.db")
if "postgres://" in db_url:
    db_url = db_url.replace("postgres://", "postgresql://")

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app, resources={r"/*": {"origins": "*"}})  
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/users', methods=['GET'])
def get_users():
    users = Users.query.all()
    response = [user.serialize() for user in users]
    return jsonify({"message": "ok", "results": response}), 200

@app.route('/users/favorites/<int:user_id>', methods=['GET'])
def get_user_favorites(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"message": "error", "error": "User not found"}), 404

    favorites = Favorites.query.filter_by(user_id=user_id).all()
    response = [favorite.serialize() for favorite in favorites]
    return jsonify({"message": "ok", "results": response}), 200

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    response = [person.serialize() for person in people]
    return jsonify({"message": "ok", "results": response}), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    if not person:
        return jsonify({"message": "error", "error": "Character not found"}), 404
    return jsonify({"message": "ok", "result": person.serialize()}), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    response = [planet.serialize() for planet in planets]
    return jsonify({"message": "ok", "results": response}), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if not planet:
        return jsonify({"message": "error", "error": "Planet not found"}), 404
    return jsonify({"message": "ok", "result": planet.serialize()}), 200

@app.route('/favorite/planet/<int:user_id>/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    user = Users.query.get(user_id)
    planet = Planets.query.get(planet_id)

    if not user:
        return jsonify({"message": "error", "error": "User not found"}), 404
    if not planet:
        return jsonify({"message": "error", "error": "Planet not found"}), 404

    existing_favorite = Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if existing_favorite:
        return jsonify({"message": "error", "error": "Planet already in favorites"}), 400

    new_favorite = Favorites(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"message": "Planet added to favorites"}), 201

@app.route('/favorite/people/<int:user_id>/<int:people_id>', methods=['POST'])
def add_favorite_people(user_id, people_id):
    user = Users.query.get(user_id)
    person = People.query.get(people_id)

    if not user:
        return jsonify({"message": "error", "error": "User not found"}), 404
    if not person:
        return jsonify({"message": "error", "error": "Character not found"}), 404

    existing_favorite = Favorites.query.filter_by(user_id=user_id, people_id=people_id).first()
    if existing_favorite:
        return jsonify({"message": "error", "error": "Character already in favorites"}), 400

    new_favorite = Favorites(user_id=user_id, people_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"message": "Character added to favorites"}), 201

@app.route('/favorite/planet/<int:user_id>/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    favorite = Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()

    if not favorite:
        return jsonify({"message": "error", "error": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite deleted"}), 200

@app.route('/favorite/people/<int:user_id>/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(user_id, people_id):
    favorite = Favorites.query.filter_by(user_id=user_id, people_id=people_id).first()

    if not favorite:
        return jsonify({"message": "error", "error": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite deleted"}), 200

@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response"
    }
    return jsonify(response_body), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)  
