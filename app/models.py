"""
Creating models for the SQL database.
"""
from app import db

class User(db.Model):
    """
    The users table.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    phone_num = db.Column(db.String(64), index=True, unique=True)
    # Connect a primary key to a foreign key to create one-to-many relationship.
    subreddits = db.relationship('Subreddit', backref='user', lazy='dynamic')

    # __repr__ tells Python how to print objects of this class.
    def __repr__(self):
        return '<User {}>'.format(self.username)

class Subreddit(db.Model):
    """
    The subreddits table.
    """
    id = db.Column(db.Integer, primary_key=True)
    subreddit_name = db.Column(db.String(128), index=True, unique=True)
    # Connect a foreign key to a primary key.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # Connect a primary key to a foreign key to create one-to-many relationship.
    keywords = db.relationship('Keyword', backref='subreddit', lazy='dynamic')

    def __repr__(self):
        return '<Subreddit {}>'.format(self.subreddit_name)

class Keyword(db.Model):
    """
    The keywords table.
    """
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(128), index=True, unique=True)
    # Connect a foreign key to a primary key.
    subreddit_id = db.Column(db.Integer, db.ForeignKey('subreddit.id'))

    def __repr__(self):
        return '<Keyword {}>'.format(self.keyword)

