from flask import request
from uuid import uuid4
from flask.views import MethodView
from flask_smorest import abort

from schemas import PostSchema

#imports from app folder
from . import bp
from db import posts


########## post routes  #####################


@bp.route('/') #get/retrieve info
class PostList(MethodView):


  def get(self): #changed get_post to get
      post_data = request.get_json()
      return jsonify(posts), 200



  #highlights, name, location, user_id required
  #create/send
  @bp.arguments(PostSchema)
  def post(self, post_data): #changed create_post to post
    #post_data = request.get_json()
      # if 'name' not in post_data or 'location' not in post_data or 'highlights' not in post_data or 'user_id' not in post_data:
    #     abort(400, message='Please include body and user id')
    posts[uuid4().hex ] = post_data
    return post_data, 201

  


@bp.route('/<post_id>') #edit/update
class Post(MethodView):

  
  def get(self, post_id): #route to get one user, changed get_posts to get
    try:
        post = posts[post_id]
        return post, 200
    except KeyError:
        abort(404, message='Post not Found') #flask smorest
        #return {'message': 'user not found'}, 400


  @bp.arguments(PostSchema)
  def put(self, post_data, post_id): #changed edit_post to put, post_data comes before dynamic url (ex slug)
    #post_data = request.get_json()
    if post_id in posts:
      post = posts[post_id]
      if post_data['user_id'] != post['user_id']:
         abort(400, message = 'Cannot edit other users post')
      post['name'] = post_data['name']
      post['location'] = post_data['location']
      post['highlights'] = post_data['highlights']
      return post, 200
    abort(404, message='Post not Found')
    #return {'message': 'Post not found'}, 400


  def delete(self,post_id): #changed delete_post to delete
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

