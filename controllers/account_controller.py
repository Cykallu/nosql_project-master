from flask_jwt_extended import jwt_required, get_jwt
from flask import  jsonify, request
from models import User
from validators.Account import validate_account, validate_account_password_route_handler, check_profile_picture_max_size
from passlib.hash import pbkdf2_sha256 as sha256

@jwt_required()
@validate_account
def account_route_handler():
    if request.method == 'GET':
        logged_in_user = get_jwt()
        account = User.get_by_id(logged_in_user['sub'])
        return jsonify(account=account.to_json())
    
    elif request.method == 'PATCH':
        logged_in_user = get_jwt()
        account = User.get_by_id(logged_in_user['sub'])
        request_body = request.get_json()
        if request_body:
            if 'username' in request_body:
                username = request_body['username']
                account.username = username
                account.update()
                return jsonify(account=account.to_json())
            raise ValidationError(message='username is required')
        raise ValidationError(message='request body is required')



@jwt_required()
@validate_account_password_route_handler
def update_account_password_route_handler():
    if request.method == 'PATCH':
        request_body = request.get_json()
        logged_in_user = get_jwt()
        account = User.get_by_id(logged_in_user['sub'])
        new_password = request_body['password']
        account.password = sha256.hash(new_password)
        account.update()
        return jsonify(account=account.to_json())

@jwt_required()
@check_profile_picture_max_size(max_size_in_kt=200)
def update_profile_picture_route_handler():
    if request.method == 'PATCH':
        request_body = request.to_json()
        logged_in_user = get_jwt()
        account = User.get_by_id(logged_in_user['sub'])
        new_prof_pic = request_body['profile_picture']
        account.profile_picture = new_prof_pic
        account.update()
        return jsonify(account=account.to_json())

