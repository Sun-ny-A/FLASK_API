from flask import request #third party imports at top
from flask.views import MethodView
from uuid import uuid4
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError

from schemas import PostSchema, UpdateUserSchema, UserSchema

from . import bp
from .UserModel import UserModel
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

    @bp.response(200, UserSchema)
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


    # #also rework user variable
    # #edit/update info, <> slug for unique endpoint, default str
    # @bp.response(200, UserSchema)
    # @bp.arguments(UpdateUserSchema)
    # def put(self, user_data, user_id): #update_user changed to put
    #     user_data = request.get_json()
    #     try:
    #         user = users[user_id]
    #         if user['password'] != user_data['password']:
    #             abort(400, message='Incorrect Password')
    #         #user.update(user_data)
    #         user |= user_data   #|= is shorthand to update a dict ---> user.update(user_data)
    #         if 'new_password' in user_data:
    #             new_password = user.pop('new_password')
    #             user['password'] = new_password
    #         return user, 200
    #     except KeyError:
    #         abort(404, message='Post not Found')
    #         #return {'message': 'user not found'}, 400


    #get all posts for an individual user
    @bp.get('/user/<user_id>/post')
    @bp.response(200, PostSchema(many=True))
    def get_user_posts(user_id):
        if user_id not in users:
            abort(404, message='Post not Found')
            #return {'message': 'user not found'}, 400
        user_posts = [{'name':post['name'], 'location':post['location'], 'highlights':post['highlights']}
            for post in posts.values()
            if post['user_id'] == user_id]
        return {'user_posts': user_posts}, 200




    

######### HELP
# #get all posts for an individual user
# #@bp.get('/user/<user_id>/post')
# def get_user_posts(user_id):
#   if user_id not in users:
#     abort(404, message='Post not Found')
#     #return {'message': 'user not found'}, 400
#   user_posts = [{'name':post['name'], 'location':post['location'], 'highlights':post['highlights']}
#     for post in posts.values() 
#     if post['user_id'] == user_id]
#   return {'user_posts': user_posts}, 200


# #add new user
# @app.post('/user') #create/send info
# def create_user():
#   user_data = request.get_json() #created username and email
#   user_data['country'] = [] #to add country into data create a dict
#   users.append(user_data) #append new person's info to users
#   print(users)
#   return user_data, 201


# #delete item in highlight list
# def delete(self): #renamed delete_user to delete
#     user_data = request.get_json()
#     for user in users:
#         for get_country in user.get('country', []): #use .get to ouput value of a dict, country values are a list of dicts
#             if 'highlights' in get_country:
#                 if 'skiing' in get_country['highlights']:
#                     get_country['highlights'].remove('skiing')
#     return {'message':f'Skiing is deleted'}, 202


# #changed users from list of dicts to dicts and deleted country
# @bp.post('/user') #create/send info
# def create_user():
#   user_data = request.get_json() #country no longer in users dict, in posts
#   user_data[uuid4().hex] = user_data 
#   return user_data, 201


#update name of a country
# @app.put('/user') #edit/update info
# def update_user():
#     user_data = request.get_json()
#     new_name = user_data.get('new name') #.get = built in function that outputs a dict value
#     for user in users:
#         if 'country' in user and 'name' in user['country'][0] and user['country'][0]['name'] == 'Cuba':
#             user['country'][0]['name'] = new_name
#             return user, 200
#     return user, 200



    
#second approach to upate_user
# def update_user(user_id):
#   user_data = request.get_json()
#   if user_id in users:
#     user = users[user_id]
#     return user, 201
#   return {'message': 'user not found'}, 400


    
    
    #error code
    # for i, user in enumerate(users):
    #     if user['country']['highlights'][0] == user_data['country']['highlights'][0]:
    #         users['country']['highlights'][0].pop()
    #         print(users)
    # return {'message':f'{user_data["country"]["highlights"][0]} is deleted'}, 202
