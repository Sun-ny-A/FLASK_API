from flask_smorest import Blueprint

#make a instance of blueprint
bp = Blueprint('users', __name__, description='Ops on Users')

from . import routes #. is from current directory
from . import auth_routes