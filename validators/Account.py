from errors.validation_error import ValidationError
from flask import request


def validate_account(account_route_handler_func):
    def validate_account_wrapper(*args, **kwargs):
        request_body = request.get_json()
        if request.method == 'GET':
            return account_route_handler_func(*args, **kwargs)
        elif request.method == 'PATCH':
            # mennään tänne, jos request_body lähetetään insomniasta
            if request_body:
                # jos username-kenttä löytyy requst_bodysta,
                # kaikki on kunnossa ja voidaan mennä eteenpäin account_route_handleriin
                if 'username' in request_body:
                    return account_route_handler_func(*args, **kwargs)
                else:
                    # jos username ei ole request_bodyssa, siitä nostetaan virhe
                    raise ValidationError('Username is required')
            else:
                # tänne mennään, jos request bodya ei ole edes lähetetty (vasen sarake insomniassa)
                raise ValidationError('Body is required')
    return validate_account_wrapper

def validate_account_password_route_handler(f):
    def validate_account_password_route_handler_wrapper(*args,**kwargs):
        request_body = request.get_json()
        if request.method == 'PATCH':
            if request_body:
                if 'password' in request_body:
                    return validate_account_password_route_handler(*args, **kwargs)
        else:
            return f(*args, **kwargs)
    return validate_account_password_route_handler_wrapper


def validate_update_profile_picture(func):
    def validate_update_profile_picture_wrapper(*args, **kwargs):
        request_body = request.get_json()
        if request.method == 'PATCH':
            if request_body:
                if 'profile_picture' in request_body:
                    return validate_update_profile_picture(*args, **kwargs)
        else:
            return func(*args, **kwargs)
    return validate_update_profile_picture_wrapper

def check_profile_picture_max_size(max_size_in_kt = 100):
    def check_profile_picture_max_size_wrapper(func):
        def wrapper(*args, **kwargs):
            request_body = request.get_json()
            profile_pic = request_body['profile_picture']
            pic_to_bytes = (len(profile_pic)*3)/4
            size_in_kt = pic_to_bytes/1024
            if request_body:
                if 'profile_picture' in request_body:
                    if size_in_kt <= max_size_in_kt:
                        return func(*args, **kwargs)
        return wrapper
    return check_profile_picture_max_size_wrapper                    



        