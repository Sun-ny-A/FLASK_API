from flask import request #third party imports at top
from flask.views import MethodView
from uuid import uuid4
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError

from schemas import PostSchema, UpdateUserSchema, UserSchema, UserSchemaNested

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
    # def get(self): #renamed get_users to get
    #     return users.values() # status code here no longer needed if in response
    def get(self):
        users = UserModel.query.all()
        return users


    def delete(self):
        user_data = request.get_json()
        user= UserModel.query.filter_by(username=user_data['username']).first()
        if user and user.check_password(user_data['password']):
            user.delete()
            return {'message':f'{user_data["username"]} deleted'}, 202
        abort(400, 'Username or password invalid')


    #update to add password
    @bp.arguments(UserSchema)   #always argument first then response, arguments validates info coming in and values need to be str
    @bp.response(201, UserSchema)   #response serializes info going out
    def post(self, user_data): #renamed create_user to post
        #user_data = request.get_json()     #schema now collecting user_data
        # for k in ['username', 'email', 'password']:
        #     if k not in user_data:
        #         abort(400, message='Please include username, email and password')
        #users[uuid4().hex] = user_data
        user = UserModel()
        user.from_dict(user_data)
        db.session.add(user)
        db.session.committ()
        # password = user_data.pop('password')
        # user.hash_password(password)
        try:
            user.save() #user is accessing methods
            return user_data
        except IntegrityError:
            abort(400, message='Username or email already taken.')




#route to get one user
@bp.route('/user/<user_id>')
class User(MethodView):

    @bp.response(200, UserSchemaNested)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id, description='User Not Found')
        return user

    # def get(self, user_id): #get_user changed to get
    #     try:
    #         user = users[user_id]
    #         return user
    #     except KeyError:
    #         abort(404, message='User not Found')
    #         #return {'message': 'user not found'}, 400


    @bp.arguments(UpdateUserSchema)
    @bp.response(202, UserSchema)
    def put(self, user_data, user_id):
        user = UserModel.query.get_or_404(user_id, description='User Not Found')
        if user and user.check_password(user_data['password']):
            try:
                user.from_dict(user_data)
                user.save()
                return user
            except IntegrityError:
                abort(400, message='Username or Email already Taken')



    # #get all posts for an individual user
    # @bp.get('/user/<user_id>/post')
    # @bp.response(200, PostSchema(many=True))
    # def get_user_posts(user_id):
    #     if user_id not in users:
    #         abort(404, message='Post not Found')
    #         #return {'message': 'user not found'}, 400
    #     user_posts = [{'name':post['name'], 'location':post['location'], 'highlights':post['highlights']}
    #         for post in posts.values()
    #         if post['user_id'] == user_id]
    #     return {'user_posts': user_posts}, 200



@bp.route('/user/follow/<follower_id>/<followed_id>')
class FollowUser(MethodView):

    
    @bp.response(200, UserSchema(many=True))
    def post(self, follower_id, followed_id):
        user = UserModel.query.get(follower_id)
        user_to_follow = UserModel.query.get(followed_id)
        if user and user_to_follow:
            user.follow_user(user_to_follow)
            return user.followed.all()
        abort(400, message='Invalid user info')


    def put(self, follower_id, followed_id):
        user = UserModel.query.get(follower_id)
        user_to_unfollow = UserModel.query.get(followed_id)
        if user and user_to_unfollow:
            user.unfollow_user(user_to_unfollow)
            return {'message': f'User: {user_to_unfollow.username} unfollowed'}, 202
        abort(400, message='Invalid user info') 