"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users, People, Planets, Startships, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# PEOPLE
@app.route('/people', methods=['GET'])
def get_all_people():
    query_results = People.query.all()
    results = list(map(lambda people: people.serialize(),query_results))
    if results != []:
        response_body = {
            "msg": "Ok",
            "results": results
        }
        return jsonify(response_body), 200
    else: 
        return jsonify({"msg": "There aren't any people yet"}), 404

@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_people(people_id):
    query_result = People.query.filter_by(id=people_id).first()
    
    if query_result is not None:
        response_body = {
            "msg": "Ok",
            "result":  query_result.serialize()
        }
        return jsonify(response_body), 200
    else: 
        return jsonify({"msg": f"There isn't any people with the id: {people_id}"}), 404

# @app.route('/people/<int:people_id>', methods=['DELETE'])
# def delete_one_people(people_id):
#     query_result = People.query.filter_by(id=people_id).first()
    
#     if query_result is not None:
#         response_body = {
#             "msg": "Ok",
#             "result":  query_result.serialize()
#         }
#         return jsonify(response_body), 200
#     else: 
        # return jsonify({"msg": f"There isn't any people with the id: {people_id}"}), 404

# PLANETS
@app.route('/planets', methods=['GET'])
def get_all_planets():
    query_results = Planets.query.all()
    results = list(map(lambda planet: planet.serialize(),query_results))
    if results != []:
        response_body = {
            "msg": "Ok",
            "results": results
        }
        return jsonify(response_body), 200
    else: 
        return jsonify({"msg": "There aren't any planet yet"}), 404

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    query_result = Planets.query.filter_by(id=planet_id).first()
    
    if query_result is not None:
        response_body = {
            "msg": "Ok",
            "result":  query_result.serialize()
        }
        return jsonify(response_body), 200
    else: 
        return jsonify({"msg": f"There isn't any planet with the id: {planet_id}"}), 404
    
# STARTSHIPS    
@app.route('/startships', methods=['GET'])
def get_all_startships():
    query_results = Startships.query.all()
    results = list(map(lambda startship: startship.serialize(),query_results))
    if results != []:
        response_body = {
            "msg": "Ok",
            "results": results
        }
        return jsonify(response_body), 200
    else: 
        return jsonify({"msg": "There aren't any startships yet"}), 404

@app.route('/startship/<int:startship_id>', methods=['GET'])
def get_one_startship(startship_id):
    query_result = Startships.query.filter_by(id=startship_id).first()
    
    if query_result is not None:
        response_body = {
            "msg": "Ok",
            "result":  query_result.serialize()
        }
        return jsonify(response_body), 200
    else: 
        return jsonify({"msg": f"There isn't any startship with the id: {startship_id}"}), 404

# USERS
@app.route('/users', methods=['GET'])
def get_all_users():
    query_results = Users.query.all()
    results = list(map(lambda user: user.serialize(),query_results))
    if results != []:
        response_body = {
            "msg": "Ok",
            "results": results
        }
        return jsonify(response_body), 200
    else: 
        return jsonify({"msg": "There aren't any users yet"}), 404

# FAVORITES
@app.route('/users/favorites/<int:users_id>', methods=['GET'])
def get_all_favorites(users_id):
    query_results = Favorites.query.filter_by(users_id=users_id).all()
    if query_results:
        # results = [favorite.serialize() for favorite in query_results]
        results = list(map(lambda item: item.serialize(),query_results))
        print(results)
        return jsonify({"msg": "Ok", "results": results}), 200
    else:
        return jsonify({"msg": "There aren't any favorites yet"}), 404


@app.route('/favorite/planet/<int:planets_id>', methods=['POST'])
def add_favorite_planet(planets_id):
    data = request.json
    user_exist = Users.query.filter_by(id=data["users_id"]).first()
    planet_exist = Planets.query.filter_by(id=data["planets_id"]).first()

    if user_exist and planet_exist:
        query_results = Favorites.query.filter_by(planets_id=data["planets_id"], users_id=data["users_id"]).first()
        print(query_results)
        if query_results is None:
            new_favorite = Favorites(planets_id=data["planets_id"], users_id=data["users_id"])
            db.session.add(new_favorite)
            db.session.commit()
            return ({"msg": "Ok"}),200
        else:
             return ({"msg": "Favorites already exists"}), 200
        
    elif user_exist is None and planet_exist is None:
        return ({"msg": "There aren't users or planets"}), 400 
    elif user_exist is None:
        return ({"msg": "This user doesn't exist"}), 400
    elif planet_exist is None:
        return ({"msg": "This planet doesn't exist"}), 400

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    data = request.json
    user_exist = Users.query.filter_by(id=data["users_id"]).first()
    planet_exist = People.query.filter_by(id=data["people_id"]).first()

    if user_exist and planet_exist:
        query_results = Favorites.query.filter_by(people_id=data["people_id"], users_id=data["users_id"]).first()
        print(query_results)
        if query_results is None:
            new_favorite = Favorites(people_id=data["people_id"], users_id=data["users_id"])
            db.session.add(new_favorite)
            db.session.commit()
            return ({"msg": "Ok"}),200
        else:
             return ({"msg": "Favorites already exists"}), 200
        
    elif user_exist is None and people_id is None:
        return ({"msg": "There aren't users or people"}), 400 
    elif user_exist is None:
        return ({"msg": "This user doesn't exist"}), 400
    elif planet_exist is None:
        return ({"msg": "This people doesn't exist"}), 400


# [DELETE] /favorite/planet/<int:planet_id>
@app.route('/favorite/planet/<int:planets_id>', methods=['DELETE'])
def delete_favorite_planet(planets_id):
    data = request.json
    user_exist = Users.query.filter_by(id=data["users_id"]).first()
    planet_exist = Planets.query.filter_by(id=data["planets_id"]).first()

    if planet_exist and user_exist:
        query_results = Favorites.query.filter_by(planets_id=data["planets_id"], users_id=data["users_id"]).first()
        print(query_results)
        if query_results:
            db.session.delete(query_results)
            db.session.commit()
            return ({"msg": "Favorite deleted"}),200
        else: return ({"msg": "This favorite doesn't exist"}),404
        
    elif user_exist is None and planet_exist is None:
        return ({"msg": "There aren't users or planets"}), 400 
    elif user_exist is None:
        return ({"msg": "This user doesn't exist"}), 400
    elif planet_exist is None:
        return ({"msg": "This planet doesn't exist"}), 400
    
# [DELETE] /favorite/people/<int:people_id>
@app.route('/favorite/people/<int:people_id>/<int:users_id>', methods=['DELETE'])
def delete_favorite_people_user(people_id, users_id):
    user_exist = Users.query.filter_by(id=users_id).first()
    people_exist = People.query.filter_by(id=people_id).first()

    if user_exist and people_exist:
        query_results = Favorites.query.filter_by(people_id=people_id, users_id=users_id).first()
        print(query_results)
   
        if query_results:
            db.session.delete(query_results)
            db.session.commit()
            return ({"msg": "Deleted succesfull"}), 200
        else:
            return ({"msg": "Character already deleted"}), 200
        
    elif user_exist is None and people_exist is None:
        return ({"msg": "There aren't users or characters to delete"}), 400
  
    elif user_exist is None:
        return ({"msg": "This user doesn't exist"}), 400

    elif people_exist is None:
        return ({"msg": "This character doesn't exist"}), 400

# [PUT] /people/<int:people_id>
@app.route('/people/<int:people_id>', methods=['PUT'])
def update_people(people_id):
        new_data = request.json
        query_results = People.query.filter_by(id=people_id).first()
        print(query_results)
        if query_results:
            for key, value in new_data.items():
                setattr(query_results, key, value)
            db.session.commit()
            return ({"msg": "People updated"}), 200
        else: return ({"msg": "People can't updated"}), 404    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
