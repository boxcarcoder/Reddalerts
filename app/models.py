"""
Models for the SQL database.
"""
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.inspection import inspect
# from sqlalchemy_utils import auto_delete_orphans
# for deleting many-to-many "orphans".
# from sqlalchemy import event, create_engine
# from sqlalchemy.orm import attributes, sessionmaker

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

"""
An association table between the users and subreddits tables to create
a many-to-many relationship.
"""
users_subreddits = db.Table('users_subreddits',
    # Place the users and subreddits foreign key into the table.
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE')),
    db.Column('subreddit_id', db.Integer, db.ForeignKey('subreddits.id',  ondelete='CASCADE'))
)

# old structure that may include fluff?
# users_subreddits = db.Table('users_subreddits',
#     db.Column('id', db.Integer, primary_key=True),
#     # Place the users and subreddits foreign key into the table.
#     db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE')),
#     db.Column('subreddit_id', db.Integer, db.ForeignKey('subreddits.id',  ondelete='CASCADE'))
# )

class User(db.Model, JsonSerializer):
    """
    The users table.
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    phone_num = db.Column(db.String(64), index=True, unique=True)
    received_posts = db.Column(db.String(128), index=True, unique=True)

    # Establish a "parent-children" relationship (user -> subreddits).
    subreddits = db.relationship('Subreddit', secondary=users_subreddits, backref='users', cascade='all, delete', lazy='dynamic')

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

    """ Override serializer to delete Subreddits from User instances """
    def serialize(self):
        dictionary = JsonSerializer.serialize(self)
        del dictionary["subreddits"]
        return dictionary

"""
An association table between the subreddits and keywords tables to create
a many-to-many relationship.
"""
subreddits_keywords = db.Table('subreddits_keywords', db.Model.metadata,
    # Place the subreddits and keywords foreign keys in the table.
    db.Column('subreddit_id', db.Integer, db.ForeignKey('subreddits.id', ondelete='CASCADE')),
    db.Column('keyword_id', db.Integer, db.ForeignKey('keywords.id',  ondelete='CASCADE')),
)

class Subreddit(db.Model, JsonSerializer):
    """
    The subreddits table.
    """
    
    __tablename__ = 'subreddits'

    id = db.Column(db.Integer, primary_key=True)
    subreddit_name = db.Column(db.String(128), index=True)

    # Establish a "parent-children" relationship (subreddit -> keywords).
    keywords = db.relationship('Keyword', secondary=subreddits_keywords, backref='subreddits', cascade='all, delete', lazy='dynamic')

    """ Constructor """
    def __init__(self, subreddit_name):
        self.subreddit_name = subreddit_name
        self.active = True

    """ Print function """
    def __repr__(self):
        return '<Subreddit {}>'.format(self.subreddit_name)

    """ Override serializer to serialize the Keywords in each Subreddit instance. Delete Users from each Subreddit since client does not need it. """
    def serialize(self):
        dictionary = JsonSerializer.serialize(self)
        del dictionary["users"]

        # Grab the AppenderBaseQuery object assigned to keywords
        values = dictionary["keywords"]

        # Serialize each keyword-AppenderBaseQuery-object into JSON format
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
    keyword = db.Column(db.String(128), index=True)

    """ Constructor """
    def __init__(self, keyword):
        self.keyword = keyword
        self.active = True

    """ Print function """
    def __repr__(self):
        return '<Keyword {}>'.format(self.keyword)

    """ Override serializer to delete the Subreddits from Keyword during serialization since we do not need to send them to the client.  """
    def serialize(self):
        dictionary = JsonSerializer.serialize(self)
        del dictionary["subreddits"]
        return dictionary



# migrate to routes?
# test without self parameter.
def check_for_keyword_orphans(self, keyword):
    # check if each keyword has an associated subreddit
    if len(keyword.subreddits) == 0:
        self.session.delete(keyword)
        return True # keyword deleted
    else:
        return False # keyword still has associated subreddit


# engine = create_engine("mysql://", echo=True)
# Session = sessionmaker(bind=engine)

# @event.listens_for(Session, 'after_flush')
# def delete_tag_orphans(session, ctx):
#     # optional: look through Session state to see if we want
#     # to emit a DELETE for orphan Tags
#     flag = False

#     for instance in session.dirty:
#         if isinstance(instance, Subreddit) and \
#             attributes.get_history(instance, 'keywords').deleted:
#             flag = True
#             break
#     for instance in session.deleted:
#         if isinstance(instance, Subreddit):
#             flag = True
#             break

#     # emit a DELETE for all orphan Tags.   This is safe to emit
#     # regardless of "flag", if a less verbose approach is
#     # desired.
#     if flag:
#         session.query(Keyword).\
#             filter(~Keyword.subreddits.any()).\
#             delete(synchronize_session=False)


# auto_delete_orphans(Subreddit.keywords)
