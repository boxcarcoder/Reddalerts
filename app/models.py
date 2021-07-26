"""
Models for the SQL database.
"""
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.inspection import inspect

class JsonSerializer(object):
    def serialize(self):
        dictionary = dict()
        for key in inspect(self).attrs.keys():
            value = getattr(self, key)
            dictionary[key] = value

        return dictionary
  
    @staticmethod
    def serialize_list(l):
        return [entry.serialize() for entry in l]


class User(db.Model, JsonSerializer):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    phone_num = db.Column(db.String(64), index=True, unique=True)
    received_posts = db.Column(db.String(128), index=True, unique=True)

    # monitor = db.relationship('Monitor', back_populates='user')

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

    # Overload serializer to delete Monitor column from a user object during serialization.
    def serialize(self):
        dictionary = JsonSerializer.serialize(self)
        del dictionary["monitors"] 
        return dictionary


class Subreddit(db.Model, JsonSerializer):
    __tablename__ = 'subreddits'

    id = db.Column(db.Integer, primary_key=True)
    subreddit_name = db.Column(db.String(128), index=True)

    """
    Helper Functions.
    """
    # Constructor
    def __init__(self, subreddit_name):
        self.subreddit_name = subreddit_name
        self.active = True

    # Print Function
    def __repr__(self):
        return '<Subreddit {}>'.format(self.subreddit_name)

    def serialize(self):
        dictionary = JsonSerializer.serialize(self)
        del dictionary["monitors"]
        return dictionary


class Keyword(db.Model, JsonSerializer):
    __tablename__ = 'keywords'

    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(128), index=True)

    # monitor = db.relationship('Monitor', back_populates='keyword')

    """
    Helper Functions.
    """
    # Constructor
    def __init__(self, keyword):
        self.keyword = keyword
        self.active = True

   # Print Function
    def __repr__(self):
        return '<Keyword {}>'.format(self.keyword)

    def serialize(self):
        dictionary = JsonSerializer.serialize(self)
        return dictionary


class Monitor(db.Model):
    __table_name__ = 'monitors'

    id = db.Column(db.Integer, primary_key=True)

    # Enable relationship between monitor <-> user.
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    # Establish a collection of User objects on Monitor. (Monitor.user)
    user = db.relationship('User', backref='monitors')

    # Enable relationship monitor <-> subreddit.
    subreddit_id = db.Column(db.Integer, db.ForeignKey("subreddits.id"), nullable=True)
    # Establish a collection of Subreddit objects on Monitor.
    subreddit = db.relationship('Subreddit', backref='monitors')

    # Enable relationship between monitor <-> keyword.    
    keyword_id = db.Column(db.Integer, db.ForeignKey("keywords.id"), nullable=True)
    # Establish a collection of Keyword objects on Monitor.
    keyword = db.relationship('Keyword', backref='monitors')

    # user = db.relationship('User', back_populates='monitor')
    # subreddit = db.relationship('Subreddit')
    # keyword = db.relationship('Keyword', back_populates='monitor')

    def __repr__(self):
        return "<Monitor(%s)>".format(self)








#####

# """
# An association table between the users and subreddits tables to create
# a many-to-many relationship (two one-to-many relationships).
# Each record will contain a match field that contains the value 
# of each foreign key.
# """
# users_subreddits = db.Table('users_subreddits',
#     # Place the users and subreddits foreign key into the table.
#     db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE')),
#     db.Column('subreddit_id', db.Integer, db.ForeignKey('subreddits.id',  ondelete='CASCADE'))
# )



# """
# An association table between the subreddits and keywords tables to create
# a many-to-many relationship.
# """
# subreddits_keywords = db.Table('subreddits_keywords', db.Model.metadata,
#     # Place the subreddits and keywords foreign keys in the table.
#     db.Column('subreddit_id', db.Integer, db.ForeignKey('subreddits.id', ondelete='CASCADE')),
#     db.Column('keyword_id', db.Integer, db.ForeignKey('keywords.id',  ondelete='CASCADE')),
# )
