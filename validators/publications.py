from errors.unauthorized import Unauthorized
from flask import  jsonify, request
from flask_jwt_extended import get_jwt

def validate_publication_route_handler(publication_route_handler):
    def validate_update_publication_wrapper(*args, **kwargs):
        if request.method == 'GET':
            return publication_route_handler(*args, **kwargs)
        elif request.method == 'PATCH':
            logged_in_user = get_jwt()
            if not logged_in_user:
                raise Unauthorized()

            request_body = request.get_json()
            if not request_body:
                raise ValidationError('request body is required')
            if 'title' not in request_body:
                raise ValidationError('title is required')
            if 'description' not in request_body:
                raise ValidationError('description is required')
            if 'visibility' not in request_body:
                raise ValidationError('visibility is required')
            return publication_route_handler(*args, **kwargs)
        
        elif request.method == 'DELETE':
            logged_in_user = get_jwt
            if not logged_in_user:
                raise Unauthorized()
            else:
                return publication_route_handler(*args, **kwargs)
    return validate_update_publication_wrapper


