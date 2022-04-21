from urllib import request
from flask_jwt_extended import jwt_required, get_jwt
from flask import  jsonify, request
from models import User
from validators.Account import validate_account

@jwt_required()
@validate_account
def account_route_handler():
    if request.method == 'GET':
        logged_in_user = get_jwt()
        account = User.get_by_id(logged_in_user['sub'])
        return jsonify(account=account.to_json())
    
    elif request.method == 'PATCH':
        request_body = request.to_json()
        logged_in_user = get_jwt()
        account = User.get_by_id(logged_in_user['sub'])
        new_username = request_body['username']
        account.username = new_username
        account = User.update()
        return jsonify(account=account.to_json())