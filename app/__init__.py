#importing from app folder runs __init__ file

from flask import Flask
app = Flask(__name__)

if __name__ == '__main__':
    app.run()

# from flask import Flask, request ---> request will give us a dict(key:value) of all the JSON(serialized and sent as a string) data getting sent

from resources.users import routes #import at bottom of file or will get errors
from resources.posts import routes
