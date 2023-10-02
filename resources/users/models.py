from app import db
from werkzeug.security import generate_password_hash, check_password_hash


#using sqlalchemy to create a table from a class

# class FollowersModel(db.Model):
#    id = db.Column(db.Integer, primary_key = True)
#    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False) #user
#    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False) #user they follow


#auxilliary table can be accessed through different queries but not actually created
#for many-to-many relationship
followers = db.Table('followers',
 db.Column('follower_id', db.Integer, db.ForeignKey ('users.id')),
 db.Column('followed_id', db.Integer, db.ForeignKey ('users.id'))
)


class UserModel(db.Model):

    __tablename__ = 'users'


    #columns
    id = db.Column(db.Integer, primary_key = True)  #primary_key = True makes it SERIAL
    username = db.Column(db.String, unique=True, nullable=False) #nullable=False username required field
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False) #store pw hash instead of pw directly
    first_name = db.Column(db.String)    #nullable=True is default, so user doesn't have to include name
    last_name = db.Column(db.String)
    posts = db.relationship('PostModel', backref='author', lazy='dynamic', cascade='all, delete') #not a column, a relationship that looks at all the posts by a user
    #backref gets user instead of user_id (int)
    #lazy=dynamic --> displays requested queries only (doesn't show all posts unless requested)
    #cascade='all, delete' --> for ex when deleting a user it will delete all posts from that user (to avoid fk contraint errors)
    followed = db.relationship('UserModel', secondary=followers, primaryjoin= followers.c.follower_id == id, secondaryjoin = followers.c.followed_id == id, backref = db.backref('followers', lazy='dynamic'), lazy = 'dynamic')

    
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
    
    def if_following(self, user):
       self.followed.filter(user.id == followers.c.followed_id).count()>0

    def follow_user(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            self.save()

    def unfollow_user(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            self.save()
    
