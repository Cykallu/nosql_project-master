from flask import jsonify, request
from models import User

from flask_jwt_extended import jwt_required
# from relation_models import User

@jwt_required()
def users_route_handler():
    if request.method == 'GET':
       users = User.get_all()
       return jsonify(users=User.list_to_json(users))
       
    elif request.method == 'POST':
        request_body = request.get_json()
        username = request_body['username']
        new_user = User(username)
        new_user.create()
        return jsonify(user=new_user.to_json())
        
     
def user_route_handler(_id):
    if request.method == 'GET':
        user = User.get_by_id(_id)
        return jsonify(user=user.to_json())
    elif request.method == 'DELETE':
        User.delete_by_id(_id)
        return ""
    
    elif request.method == 'PATCH':
        request_body = request.get_json()
        new_username = request_body['username']
        user = User.update_by_id(_id, new_username)
        return jsonify(user=user.to_json())