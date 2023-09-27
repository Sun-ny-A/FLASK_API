from flask import request #third party imports at top
from uuid import uuid4

from app import app
from db import users, posts



#heading
@app.route('/<username>')
def intro(username):
    return f"<header>Welcome to <b>Wonderlust</b>, {username}, your digital travel guide!</header>"

#get users
@app.get('/user') #get/retrieve info
def get_users():
    return {'users': users}, 200

#route to get one user
@app.get('/user/<user_id>')
def get_user(user_id):
    try:
        user = users[user_id]
        return user, 200
    except KeyError:
        return {'message': 'user not found'}, 400
    

######### HELP
#get all posts for an individual user
@app.get('/user/<user_id>/post')
def get_user_posts(user_id):
    if user_id not in users:
        return {'message': 'user not found'}, 400 
    user_posts = [post for post in posts.values() if post['user_id'] == user_id]
    return {'user_posts': user_posts}, 200


# #add new user
# @app.post('/user') #create/send info
# def create_user():
#   user_data = request.get_json() #created username and email
#   user_data['country'] = [] #to add country into data create a dict
#   users.append(user_data) #append new person's info to users
#   print(users)
#   return user_data, 201


#changed users from list of dicts to dicts and deleted country
@app.post('/user') #create/send info
def create_user():
  user_data = request.get_json() #country no longer in users dict, in posts
  user_data[uuid4().hex] = user_data 
  return user_data, 201


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


#also rework user variable
@app.put('/user/<user_id>') #edit/update info, <> slug for unique endpoint, default str
def update_user(user_id):
    user_data = request.get_json()
    try:
        user = users[user_id]
        user['username'] = user_data['username']
        return user, 200
    except KeyError:
        return {'message': 'user not found'}, 400
    
#second approach to ^^
# def update_user(user_id):
#   user_data = request.get_json()
#   if user_id in users:
#     user = users[user_id]
#     return user, 201
#   return {'message': 'user not found'}, 400


#delete item in highlight list
@app.delete('/user') #delete info
def delete_user():
    user_data = request.get_json()
    for user in users:
        for get_country in user.get('country', []): #use .get to ouput value of a dict, country values are a list of dicts
            if 'highlights' in get_country:
                if 'skiing' in get_country['highlights']:
                    get_country['highlights'].remove('skiing')
    return {'message':f'Skiing is deleted'}, 202
    
    
    #error code
    # for i, user in enumerate(users):
    #     if user['country']['highlights'][0] == user_data['country']['highlights'][0]:
    #         users['country']['highlights'][0].pop()
    #         print(users)
    # return {'message':f'{user_data["country"]["highlights"][0]} is deleted'}, 202
