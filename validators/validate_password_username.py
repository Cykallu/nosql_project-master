from flask import request 
from errors.validation_error import ValidationError


def validate_password_and_username(next):
    def validate_password_and_username_wrapper(*args, **kwargs):
        request_body = request.get_json()
        if request_body is None:
            raise ValidationError(message='Body is required')
        if 'username' not in request_body:
            raise ValidationError(message='username is required')
        if 'password' not in request_body:
            raise ValidationError(message='password is required')
        return next(*args, **kwargs)
    return validate_password_and_username_wrapper


