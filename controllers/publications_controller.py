from flask import jsonify, request
from models import Publication
from flask_jwt_extended import jwt_required, get_jwt
from bson.objectid import ObjectId

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
            pass 
        # publications_in_json_format = Publication.list_to_json(publications)
        return jsonify(publications=Publication.list_to_json(publications))
    
    elif request.method == 'POST':
        owner = None
        if logged_in_user:
            publication.owner = ObjectId(logged_in_user['sub'])   
        request_body = request.get_json()
        title = request_body['title']
        description = request_body['description']
        url = request_body['url'] 
        new_publication = Publication(title, description, url, owner=owner)
        new_publication.create()
        return jsonify(publication=new_publication.to_json())



#Route handle julkaisujen käsittelyyn ID:n perusteella    
def publication_route_handler(_id):
    #Jos GET = 1.Hakee yksittäisen julkaisun ID:n perusteella ja 2.palauttaa sen JSON muodossa
    if request.method == 'GET':
        publication = Publication.get_by_id(_id)
        return jsonify(publication=publication.to_json())
    
    #Jos DELETE = 1.Hakee julkaisun ID:n perusteella ja 2.Palauttaa tyhjää
    elif request.method == 'DELETE':
        Publication.delete_by_id(_id)
        return ""
    
    elif request.method == 'PATCH':
        request_body = request.get_json()
        new_title = request_body['title']
        new_description = request_body['description']
        publication = Publication.update_by_id(_id,new_title,new_description)
        return jsonify(publication=publication.to_json())