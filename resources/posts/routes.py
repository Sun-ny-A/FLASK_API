from flask import request
from uuid import uuid4

#imports from app folder
from app import app
from db import posts

########## post routes  #####################


@app.get('/post') #get/retrieve info
def get_post():
    return {'posts': posts}, 200


#route to get one user
@app.get('/post/<post_id>')
def get_posts(post_id):
    try:
        post = posts[post_id]
        return post, 200
    except KeyError:
        return {'message': 'user not found'}, 400


@app.post('/post') #create/send
def create_post():
   post_data = request.get_json()
   posts[uuid4().hex ] = post_data
   return post_data, 201


@app.put('/post/<post_id>') #edit/update
def edit_post(post_id):
  post_data = request.get_json()
  if post_id in posts:
   post = posts[post_id]
   post['name'] = post_data['name']
   post['location'] = post_data['location']
   post['highlights'] = post_data['highlights']
   return post, 200
  return {'message': 'Post not found'}, 400


@app.delete('/post/<post_id>')
def delete_post(post_id):
  try:
    deleted_post = posts.pop(post_id)
    return {'message': f'Name deleted: {deleted_post["name"]} \n Location deleted: {deleted_post["location"]} \n Highlights deleted: {deleted_post["highlights"]}'}, 202
  except KeyError:
    return {'message': 'Post not found'}, 400