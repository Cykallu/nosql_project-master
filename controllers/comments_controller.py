from flask.views import MethodView
from flask import jsonify, request
from models import Comment, Publication
from flask_jwt_extended import jwt_required, get_jwt

class CommentsRouteHandler(MethodView):
    @jwt_required(optional=False)
    def post (self,_id):
        Publication.get_by_id(_id)
        request_body = request.get_json()
        body = request_body['body']
        owner_id = get_jwt()['sub']
        comment = Comment(body,owner_id,_id)
        comment.create()
        return jsonify(comment=comment.to_json())
    
    
    def get(self, _id):
        publication = Publication.get_by_id(_id)
        comments = publication.get_comments()
        return jsonify(comments = Comment.list_to_json(comments))
    

class CommentRouteHandler(MethodView):
    @jwt_required(optional=False)
    def patch(self,_id,comment_id):
        logged_in_user = get_jwt()
        publication = Publication.get_by_id(_id)
        comment = publication.get_comment_by_owner_id(comment_id, logged_in_user['sub'])
        request_body = request.get_json()
        comment.body = request_body.get('body', comment.body)
        comment.update()
        return jsonify(comment=comment.to_json())
    
    def get(self,_id,comment_id):
        publication = Publication.get_by_id(_id)
        comment = publication.get_comment(comment_id)
        return jsonify(comment=comment.to_json())
    
    @jwt_required(optional=False)
    def delete(self,_id,comment_id):
        logged_in_user = get_jwt()
        publication = Publication.get_by_id(_id)
        publication.delete_comment_by_id_and_owner(comment_id, logged_in_user['sub'])
        return""