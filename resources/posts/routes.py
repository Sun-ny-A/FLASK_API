from flask import request
from uuid import uuid4
from flask.views import MethodView
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity

from resources.users.models import UserModel

from .PostModel import PostModel
from schemas import PostSchema

#imports from app folder
from . import bp
from db import posts


########## post routes  #####################


@bp.route('/') #get/retrieve info
class PostList(MethodView):


  @jwt_required()
  @bp.response(200, PostSchema(many=True)) #many=true for many posts
  def get(self): #changed get_post to get
    return PostModel.query.all()


  #create/send a post
  @jwt_required()
  @bp.arguments(PostSchema)
  @bp.response(200, PostSchema)
  def post(self, post_data):
    user_id = get_jwt_identity()
    p = PostModel(**post_data, user_id = user_id)
    try:
      p.save()
      return p
    except IndentationError:
      abort(400, message="Invalid User Id")
  



@bp.route('/<post_id>') #edit/update
class Post(MethodView):

  @jwt_required()
  @bp.response(200, PostSchema)
  def get(self, post_id): #route to get one user, changed get_posts to get
    p = PostModel.query.get(post_id)
    if p:
      return p
    abort(400, message='Invalid Post Id')


  #edit a post
  @jwt_required()
  @bp.arguments(PostSchema)
  @bp.response(200, PostSchema)
  def put(self, post_data, post_id):
    p = PostModel.query.get(post_id)
    if p and post_data['body']: #including post_data['body'] to make sure user doesn't submit an empty str (empty post)
      user_id = get_jwt_identity()
      if p.user_id == get_jwt_identity():
        p.body = post_data['body']
        p.save() #adds/commits entry
        return p
      else:
        abort(401, message='Unauthorized')
    abort(400, message='Invalid Post Data')


  @jwt_required()
  def delete(self, post_id):
     user_id = get_jwt_identity()
     p = PostModel.query.get(post_id)
     if p:
       if p.user_id == user_id:
        p.delete()
        return {'message' : 'Post Deleted'}, 202
       abort(401, message='User doesn\'t have rights')
     abort(400, message='Invalid Post Id')