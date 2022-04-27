#Importit

from controllers.account_controller import account_route_handler,update_account_password_route_handler, update_profile_picture_route_handler
from flask import Flask, jsonify
from controllers.auth_controller import LoginRouteHandler, register_route_handler
from controllers.publications_controller import publications_route_handler, publication_route_handler,like_publication_route_handler, share_publication_route_handler
from errors.not_found import NotFound
from errors.validation_error import ValidationError
from flask_jwt_extended import JWTManager
from controllers.users_controller import user_route_handler, users_route_handler



#app
app = Flask(__name__)
app.config.from_object('config.Config')
jwt = JWTManager(app)

#palauttaa error 404 json muodossa
@app.errorhandler(NotFound)
def not_found_error_handler(err):
    return jsonify(err=err.args), 404

#palauttaa validationerror 400 json muodossa
@app.errorhandler(ValidationError)
def validation_error_handler(err):
    return jsonify(err=err.args), 400

#URL reititys
app.add_url_rule('/api/users', view_func=users_route_handler, methods=['GET', 'POST'])
app.add_url_rule('/api/users/<_id>', view_func=user_route_handler, methods=['GET','DELETE', 'PATCH'])

app.add_url_rule('/api/publications', view_func=publications_route_handler, methods=['GET', 'POST'])
app.add_url_rule('/api/publications/<_id>', view_func=publication_route_handler, methods=['GET','DELETE', 'PATCH'])
app.add_url_rule('/api/publications/<_id>/like', view_func=like_publication_route_handler, methods=['PATCH'])
app.add_url_rule('/api/publications/<_id>/share', view_func=share_publication_route_handler, methods=['PATCH'])


app.add_url_rule('/api/register', view_func=register_route_handler, methods=['POST'])
app.add_url_rule('/api/login', view_func=LoginRouteHandler.as_view("login_route_handler"), methods=['POST','PATCH'])

app.add_url_rule('/api/account', view_func=account_route_handler, methods=['GET','PATCH'])
app.add_url_rule('/api/account/password', view_func=update_account_password_route_handler, methods=['PATCH'])
app.add_url_rule('/api/account/profile_picture', view_func=update_account_password_route_handler, methods=['PATCH'])


if __name__ == '__main__':
    app.run(debug=True) 
