from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from bson.objectid import ObjectId
from errors.not_found import NotFound
from errors.validation_error import ValidationError

from models import Publication

@jwt_required(optional=True)
def publications_route_handler():
    logged_in_user = get_jwt() 
    if request.method == 'GET':       
        if logged_in_user: 
            if logged_in_user['role'] == 'admin':
                publications = Publication.get_all()
            elif logged_in_user['role'] == 'user': 
                publications = Publication.get_by_owner_and_visibility(
                    user=logged_in_user,
                    visibility=[1,2])
        else:
            publications = Publication.get_by_visibility()       
        return jsonify(publications=Publication.list_to_json(publications))
    elif request.method == 'POST':
        owner = None
        if logged_in_user:
            owner = ObjectId(logged_in_user['sub'])       
        request_body = request.get_json()
        title = request_body['title']
        description = request_body['description']
        url = request_body['url']
        new_publication = Publication(title, description, url, owner=owner)
        new_publication.create()
        return jsonify(publication=new_publication.to_json())


@jwt_required()
def like_publication_route_handler(_id):
    if request.method == 'PATCH':
        logged_in_user = get_jwt()
        publication = Publication.get_by_id(_id)
        found_index = -1
        for count, user_id in enumerate(publication.likes):
            if str(user_id) == logged_in_user['sub']:
                found_index = count
                break
        if found_index > -1: 
            del publication.likes[found_index]
        else:
            publication.likes.append(ObjectId(logged_in_user['sub']))
        
        publication.like()
        return jsonify(publication=publication.to_json())

@jwt_required()
def share_publication_route_handler(_id):
    if request.method == 'PATCH':
        publication = Publication.get_by_id(_id)
        publication.share()
        return jsonify(publication=publication.to_json())


@jwt_required(optional=True)
def publication_route_handler(_id):
    if request.method == 'GET':
        publication = Publication.get_by_id(_id)
        return jsonify(publication=publication.to_json())
    elif request.method == 'DELETE':
        logged_in_user = get_jwt()
        if logged_in_user:
            if logged_in_user['role'] == 'user':
                publication = Publication.get_by_id(_id)
                if publication.owner is not None and str(publication.owner) == logged_in_user['sub']:
                    publication.delete()
                raise NotFound(message='Publication not found')
        raise NotFound(message='Publication not found')
    elif request.method == 'PATCH':
        logged_in_user = get_jwt()
        if logged_in_user:
            if logged_in_user['role'] == 'user':
                publication = Publication.get_by_id(_id)
                if publication.owner is not None and str(publication.owner) == logged_in_user['sub']:
                    request_body = request.get_json()
                    if request_body:
                        if 'title' in request_body and 'description' in request_body:
                            publication.title = request_body['title']
                            publication.description = request_body['description']
                            publication.visibility = request_body['visibility']
                            publication.update()
                            return jsonify(publication=publication.to_json())
                        raise ValidationError(message='Title, description and visibility are required')
                    raise ValidationError(message='Body is required')

                raise NotFound(message='Publication not found')
        raise NotFound(message='Publication not found')

