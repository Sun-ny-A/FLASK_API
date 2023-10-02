#authentication routes

from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token

from schemas import AuthUserSchema, UserSchema
from . import bp
from .models import UserModel


#these will not have the same endpoints

#to register a user
@bp.post('/register')
@bp.arguments(UserSchema)
@bp.response(201, UserSchema)
def register(user_data):
    user = UserModel()
    user.from_dict(user_data)
    try:
        user.save()
        return user_data
    except IntegrityError:
        abort(400, message='Username or email already taken.')


@bp.post('/login')
@bp.arguments(AuthUserSchema)
def login(login_info): #login with email or username
    if 'username' not in login_info and 'email' not in login_info:
        abort(400, message='Please include username or email.')
    if 'username' in login_info:
        user = UserModel.query.filter_by(username=login_info['username']).first()
    else:
        user = UserModel.query.filter_by(email=login_info['email']).first()
    if user and user.check_password(login_info['password']): #as long as user and password are valid, we will provide an access token
        access_token = create_access_token(identity=user.id)#assigning token to specific user id, generally tokens expire every 30 min
        return {'access_token':access_token}
    abort(400, message='Invald username or password.')


@bp.route('/logout')