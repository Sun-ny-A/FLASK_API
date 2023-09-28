#creating env: python -m name_venv, name_venv\scripts\activate, pip install flask

#name default should be app.py but can rename---> need to update in terminal set FLASK_API=fakebook.py (after creating virtual env and installing flask)

# from flask import Flask, request #request will give us a dict(key:value) of all the JSON(serialized and sent as a string) data getting sent
# app = Flask(__name__)

# @app.route('/index') #creating a route and specifying end point
# @app.route('/')       #created a second landing page 
# def index():          #runs function and returns it as a string
#     return 'Matrix Fakebook'

from app import app #fakebook.py is still entry point so this directs it to app folder to run flask from there
