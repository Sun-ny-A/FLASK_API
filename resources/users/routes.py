from flask import request #third party imports at top
from flask.views import MethodView
from uuid import uuid4
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError

from schemas import PostSchema, UpdateUserSchema, UserSchema, UserSchemaNested, AuthUserSchema

from . import bp
from .models import UserModel
from app import db
from db import users, posts



# #heading
@bp.route('/<username>')
def intro(username):
    return f"<header>Welcome to <b>Wonderlust</b>, {username}, your digital travel guide!</header>"

#get users
@bp.route('/user') #get/retrieve info
class UserList(MethodView): #group similar endpoints together into a class

    @bp.response(200, UserSchema(many=True)) #many=true because we're sending a collection of users
    def get(self):
        users = UserModel.query.all()
        return users

    @jwt_required()
    @bp.arguments(AuthUserSchema)
    def delete(self, user_data):
        user_id = get_jwt_identity()
        user = UserModel.query.get(user_id)
        if user and user.username == user_data['username'] and user.check_password(user_data['password']): #checking username and pw is correct before user can delete their account
            user.delete()
            return {'message':f'{user_data["username"]} deleted'}, 202
        abort(400, 'Username or password invalid')
    

    #editing a user
    @jwt_required()
    @bp.arguments(UpdateUserSchema)
    @bp.response(202, UserSchema)
    def put(self, user_data):
        user_id = get_jwt_identity()
        user = UserModel.query.get_or_404(user_id, description='User Not Found')
        if user and user.check_password(user_data['password']):
            try:
                user.from_dict(user_data)
                user.save()
                return user
            except IntegrityError:
                abort(400, message='Username or Email already Taken')



#route to get one user
@bp.route('/user/<user_id>')
class User(MethodView):

    @bp.response(200, UserSchemaNested)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id, description='User Not Found')
        return user




@bp.route('/user/follow/<follower_id>/<followed_id>')
class FollowUser(MethodView):

    
    @bp.response(200, UserSchema(many=True))
    def post(self, followed_id):
        follower_id = get_jwt_identity()
        user = UserModel.query.get(follower_id)
        user_to_follow = UserModel.query.get(followed_id)
        if user and user_to_follow:
            user.follow_user(user_to_follow)
            return user.followed.all()
        abort(400, message='Invalid user info')


    def put(self, followed_id):
        follower_id = get_jwt_identity()
        user = UserModel.query.get(follower_id)
        user_to_unfollow = UserModel.query.get(followed_id)
        if user and user_to_unfollow:
            user.unfollow_user(user_to_unfollow)
            return {'message': f'User: {user_to_unfollow.username} unfollowed'}, 202
        abort(400, message='Invalid user info') 