from app import db
from werkzeug.security import generate_password_hash, check_password_hash

#using sqlalchemy to create a table from a class


class UserModel(db.Model):

    __tablename__ = 'users'


    #columns
    id = db.Column(db.Integer, primary_key = True)  #primary_key = True makes it SERIAL
    username = db.Column(db.String, unique=True, nullable=False) #nullable=False username required field
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False) #store pw hash instead of pw directly
    first_name = db.Column(db.String)    #nullable=True is default, so user doesn't have to include name
    last_name = db.Column(db.String)

    
    def __repr__(self):
        return f'<User: {self.username}'
    
    #storing and securing pw
    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
     return check_password_hash(self.password_hash, password)
    
    #creating a user
    def from_dict(self, dict):
        password = dict.pop('password')
        self.hash_password(password)
        for k,v in dict.items():
           setattr(self, k,v )    #instance of object to assign value, property to assign value to, value of dict
    
    def save(self):
       db.session.add(self)
       db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()