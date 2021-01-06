"""
Models for the SQL database.
"""
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from sqlalchemy.inspection import inspect

class JsonSerializer(object):
    def serialize(self):
        print('THE SELF THAT IS BEING SERIALIZED: ', self)
        dictionary = dict()
        for key in inspect(self).attrs.keys():
            # print('key: ', key)
            value = getattr(self, key)
            # if key == 'keywords':
            #     value = value.all()
            dictionary[key] = value

        print('dictionary that is serialized: ', dictionary)
        return dictionary
  
    @staticmethod
    def serialize_list(l):
        return [entry.serialize() for entry in l]

"""
An association table between the users and subreddits tables to create
a many-to-many relationship.
"""
users_subreddits = db.Table('users_subreddits',
    db.Column('id', db.Integer, primary_key=True),
    # Place the users and subreddits foreign key into the table.
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('subreddit_id', db.Integer, db.ForeignKey('subreddits.id'))
)

class User(UserMixin, db.Model, JsonSerializer):
    """
    The users table.
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    phone_num = db.Column(db.String(64), index=True, unique=True)
    # Establish a parent-children relationship (user -> subreddits).
    # Add an association table with the relationship.secondary argument.
    subreddits = db.relationship('Subreddit', secondary=users_subreddits, backref='users', lazy='dynamic')

    """
    Helper Functions.
    """
    # Constructor
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.active = True
        self.password_hash = generate_password_hash(password)

    # __repr__ tells Python how to print objects of this class.
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

"""
An association table between the subreddits and keywords tables to create
a many-to-many relationship.
"""
subreddits_keywords = db.Table('subreddits_keywords',
    db.Column('id', db.Integer, primary_key=True),
    # Place the subreddits and keywords foreign keys in the table.
    db.Column('subreddit_id', db.Integer, db.ForeignKey('subreddits.id')),
    db.Column('keyword_id', db.Integer, db.ForeignKey('keywords.id'))
)

class Subreddit(db.Model, JsonSerializer):
    """
    The subreddits table.
    """
    
    __tablename__ = 'subreddits'

    id = db.Column(db.Integer, primary_key=True)
    subreddit_name = db.Column(db.String(128), index=True, unique=True)

    # Establish a parent-children relationship (subreddit -> keywords).
    keywords = db.relationship('Keyword', secondary=subreddits_keywords, backref='subreddits', lazy='dynamic')

    """ Constructor """
    def __init__(self, subreddit_name):
        self.subreddit_name = subreddit_name
        self.active = True

    """ Print function """
    def __repr__(self):
        return '<Subreddit {}>'.format(self.subreddit_name)

    """ Override serializer to handle attributes containing Flask models """
    def serialize(self):
        dictionary = JsonSerializer.serialize(self)
        values = dictionary["keywords"]
        serialized_values = []
        for value in values:
            serialized_values.append(value.serialize())
        dictionary["keywords"] = serialized_values
        return dictionary


class Keyword(db.Model, JsonSerializer):
    """
    The keywords table.
    """

    __tablename__ = 'keywords'

    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(128), index=True, unique=True)

    """ Constructor """
    def __init__(self, keyword):
        self.keyword = keyword
        self.active = True

    """ Print function """
    def __repr__(self):
        return '<Keyword {}>'.format(self.keyword)

@login.user_loader
def load_user(id):
    """
    Load a user given an ID for Flask-Login.
    Flask_Login will pass an id to this function to fetch a user.
    """
    print('called load_user')
    return User.query.get(int(id))



# class UserJsonSerializer(JsonSerializer):
#     """
#     Extend the JsonSerializer class to change the users attribute from type
#     AppenderBaseQuery to type list.
#     """
#     # __json_modifiers__ = {
#     #     'users': lambda users, _: [dict(id=user.id, username=user.username, phone_num=user.phone_num) for user in users]
#     # }
#     pass


# class SubredditJsonSerializer(JsonSerializer):
#     """
#     Extend the JsonSerializer class to change the users attribute from type
#     AppenderBaseQuery to type list.
#     """
#     __json_modifiers__ = {
#         'users': lambda users, _: [dict(id=user.id, username=user.username, phone_num=user.phone_num) for user in users]
#         # 'subreddits': lambda subreddits, _: [dict(id=subreddit.id, subreddit_name=subreddit.subreddit_name, user_id=subreddit.user_id) for subreddit in subreddits]
#     }


# class KeywordJsonSerializer(JsonSerializer):
#     """
#     Extend the JsonSerializer class to change the users attribute from type
#     AppenderBaseQuery to type list.
#     """
#     __json_modifiers__ = {
#         'subreddits': lambda subreddits, _: [dict(id=subreddit.id, subreddit_name=subreddit.subreddit_name, user_id=subreddit.user_id) for subreddit in subreddits]
#         # 'keywords': lambda keywords, _: [dict(id=keyword.id, keyword=keyword.keyword, subreddit_id=keyword.subreddit_id) for keyword in keywords]
#     }