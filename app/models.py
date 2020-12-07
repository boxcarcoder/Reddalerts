"""
Creating models for the SQL database.
"""
from app import db

# db.Model: A base class for all models from Flask-SQLAlchemy. 
# This class defines DB fields as class variables that use instances of the db.Column class.
class User(db.Model):
    """
    The user model.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    # __repr__ tells Python how to print objects of this class.
    def __repr__(self):
        return '<User {}>'.format(self.username)   