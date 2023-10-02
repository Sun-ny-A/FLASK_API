
import os #helps us locate .env file

#this may be in __init__ instead of its own folder

class Config:
  PROPAGATE_EXCEPTIONS = True   #api errors sent to flask app for debugging
  API_TITLE = 'Fakebook Rest Api'   #our name for api
  API_VERSION = 'v1'
  OPENAPI_VERSION = '3.0.3'
  OPENAPI_URL_PREFIX = '/'
  OPENAPI_SWAGGER_UI_PATH= '/'
  OPENAPI_SWAGGER_UI_URL = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
  SQLALCHEMY_DATABASE_URI = os.environ.get('SQLDATABASE_URL')
  JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") #linking to .env folder as this will have sensitive info we don't want on github
