from flask import Blueprint

bp = Blueprint('posts', __name__, url_prefix='/post') #any route registered to bp auto goes to /post

from . import routes