from flask import jsonify, request
from models import User, db
from bson.objectid import ObjectId
from flask_jwt_extended import jwt_required
# from relation_models import User

@jwt_required()
def users_route_handler():
    if request.method == 'GET':
       users = User.get_all()
       # list_to_json on static method
       # ero normaaliin jäsenfunktioon / metodiin on siinä, että
       # kutsuttaessa static methodia
       # vasemmalla puolella on luokan nimi isolla alkukirjaimella
       return jsonify(users=User.list_to_json(users))
       
    elif request.method == 'POST':
        request_body = request.get_json()
        username = request_body['username']
        new_user = User(username)
        # createssa ensimmäinen argumentti on self
        # mutta sitä ei kutsuttaessa anneta creatella, 
        # vaan self viittaa createn vasemmalla puolella
        # olevaan muuttujaan
        new_user.create()
        
        return jsonify(user=new_user.to_json())
        
     
def user_route_handler(_id):
    if request.method == 'GET':
        user = User.get_by_id(_id)
        return jsonify(user=user.to_json())
    
    elif request.method == 'DELETE':
        # user = User.get_by_id(_id)
        # user.delete()
        User.delete_by_id(_id)
        return ""
    
    elif request.method == 'PATCH':
        # 1 ota vastaan data clientiltä 
        request_body = request.get_json()
        new_username = request_body['username']
        # 2. haetaan käyttäjä annetun _id:n perusteella
        # ja päivitetään uusi käyttäjänimi
        # user = User.get_by_id(_id)
        # user.username = new_username
        # user.update()

        user = User.update_by_id(_id, new_username)

        return jsonify(user=user.to_json())