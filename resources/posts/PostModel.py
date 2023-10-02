from app import db
from datetime import datetime #for timestamp



class PostModel(db.Model):

  __tablename__ = 'posts'

  id = db.Column(db.Integer, primary_key = True) #primary key
  body = db.Column(db.String, nullable = False) #posts, nullable = False --> cannot leave field blank
  timestamp = db.Column(db.String, default = datetime.utcnow) #time of post
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False) #one-to-many relationship b/w user and posts (one user can have many posts)...so foreign key is user_id
  #in db.ForeignKey('users.id') --> users.id refers to table.primary key column (table is 'users' and pk column is 'id')

  def __repr__(self):
    return f'<Post: {self.body}>'
  
  def save(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()