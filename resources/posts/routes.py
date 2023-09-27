from flask import request
from uuid import uuid4
from flask_smorest import abort

#imports from app folder
from . import bp
from db import posts

########## post routes  #####################


@bp.get('/') #get/retrieve info
def get_post():
    return {'posts': posts}, 200

#highlights and user_id required
@bp.post('/') #create/send
def create_post():
   post_data = request.get_json()
   if 'name' not in post_data or 'location' not in post_data or 'highlights' not in post_data or 'user_id' not in post_data:
      abort(400, message='Please include body and user id')
   posts[uuid4().hex ] = post_data
   return post_data, 201




#route to get one user
@bp.get('/<post_id>')
def get_posts(post_id):
    try:
        post = posts[post_id]
        return post, 200
    except KeyError:
        abort(404, message='Post not Found') #flask smorest
        #return {'message': 'user not found'}, 400


@bp.put('/<post_id>') #edit/update
def edit_post(post_id):
  post_data = request.get_json()
  if post_id in posts:
   post = posts[post_id]
   post['name'] = post_data['name']
   post['location'] = post_data['location']
   post['highlights'] = post_data['highlights']
   return post, 200
  abort(404, message='Post not Found')
  #return {'message': 'Post not found'}, 400


@bp.delete('/<post_id>')
def delete_post(post_id):
  try:
    deleted_post = posts.pop(post_id)
    return {'message': f'Name deleted: {deleted_post["name"]} \n Location deleted: {deleted_post["location"]} \n Highlights deleted: {deleted_post["highlights"]}'}, 202
  except KeyError:
   abort(404, message='Post not Found')
   #return {'message': 'Post not found'}, 400



# @bp.post('/') #create/send
# def create_post():
#    post_data = request.get_json()
#    posts[uuid4().hex ] = post_data
#    return post_data, 201

