from flask import jsonify, request
from models import Publication
from flask_jwt_extended import jwt_required, get_jwt
from bson.objectid import ObjectId
from validators.publications import validate_publication_route_handler

#Route handler julkaisujen käsittelyyn
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
            Publication.owner = ObjectId(logged_in_user['sub'])   
        request_body = request.get_json()
        title = request_body['title']
        description = request_body['description']
        url = request_body['url'] 
        new_publication = Publication(title, description, url, owner=owner)
        new_publication.create()
        return jsonify(publication=new_publication.to_json())



#Route handle julkaisujen käsittelyyn ID:n perusteella
@jwt_required(optional = True)
@validate_publication_route_handler
def publication_route_handler(_id):
    #Jos GET = 1.Hakee yksittäisen julkaisun ID:n perusteella ja 2.palauttaa sen JSON muodossa
    if request.method == 'GET':
        publication = Publication.get_by_id(_id)
        return jsonify(publication=publication.to_json())
    
    #Jos DELETE = 1.Hakee julkaisun ID:n perusteella ja 2.Palauttaa tyhjää
    elif request.method == 'DELETE':
        logged_in_user = get_jwt()
        if logged_in_user:
            if logged_in_user['role'] == 'user':
                publication = Publication.get_by_id(_id)
                if publication.owner is not None and str(publication.owner) == logged_in_user['sub']:
                    publication.delete()
                raise NotFound(message='Publication not found')
            if logged_in_user['role'] == 'admin':
                publication = Publication.get_by_id(_id)
                Publication.delete()
            raise NotFound(message='Publication not found')


    elif request.method == 'PATCH':
        request_body = request.get_json()
        logged_in_user = get_jwt()
        if logged_in_user['role'] == 'user':
            if logged_in_user['username'] == request_body['owner']:
                publication = Publication.get_by_id_and_owner(_id,str(logged_in_user['sub']))
                new_title = request_body['title']
                new_description = request_body['description']
                new_visibility = request_body['visibility']
                publication.title = new_title
                publication.description = new_description
                publication.visibility = new_visibility
                publication = Publication.update()
                return jsonify(publication=publication.to_json())
        if logged_in_user['role'] == 'admin':
            publication = Publication.get_by_id(_id)
            new_title = request_body['title']
            new_description = request_body['description']
            new_visibility = request_body['visibility']
            publication.title = new_title
            publication.description = new_description
            publication.visibility = new_visibility
            publication = Publication.update()
            return jsonify(publication=publication.to_json())
    
@jwt_required()
def like_publication_route_handler(_id):
    if request.method == 'PATCH':
        logged_in_user = get_jwt()
        found_index = -1 
        publication = Publication.get_by_id(_id)
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
    publication = Publication.get_by_id(_id)
    publication.share()
    return jsonify(publication=publication.to_json())
