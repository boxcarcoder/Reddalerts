"""
The routes module for the Flask application.
"""
from flask import request, jsonify, Response
from app.extensions import db
from app.application import application
from app.models import User, Subreddit, Keyword, Monitor
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.exc import IntegrityError
import re
import praw
from prawcore import NotFound
from config import Config

@application.route('/', methods=['GET'])
def index():
    return '<h1>This is my flask app</h1>'

# @application.route('/index')

@application.route('/api/login', methods=['POST'])
def login():
    # Parse the incoming request
    incoming = request.get_json()
    email = incoming["email"]
    password = incoming["password"]

    # Check the database to see if the user exists. If successful, the route sends
    # a token back to the action, which stores the token into the redux state (reducer).
    user = User.query.filter_by(email=email).one()
    if user and user.check_password(password):
        # Generate a token for the user to send back to the frontend for authentication purposes.
        s = Serializer(application.config['SECRET_KEY'], expires_in=36000)
        token = s.dumps({
            'id': user.id,
            'email': user.email,
        }).decode('utf-8')

        # Return the user to the frontend in order to populate the loggedInUser redux state.
        return jsonify(token=token, user=user.serialize())
    elif user and not user.check_password(password):
        return jsonify(error=True), 401

    # If the user doesn't exist
    return jsonify(error=True), 404

@application.route('/api/register', methods=['POST'])
def register():
    # Parse the incoming request
    incoming = request.get_json()
    username = incoming["username"]
    email = incoming["email"]
    password = incoming["password"]

    # Place the user into the database.
    user = User(username, email, password)
    db.session.add(user)

    try:
        db.session.commit()
    except IntegrityError:
        return jsonify(message="User with that email already exists"), 409

    # Generate a token for the new user to send back to the frontend for authentication purposes.
    new_user = User.query.filter_by(email=incoming["email"]).one()
    s = Serializer(application.config['SECRET_KEY'], expires_in=36000)
    token = s.dumps({
        'id': new_user.id,
        'email': new_user.email,
    }).decode('utf-8')
    return jsonify(
        token=token,
        user=new_user.serialize()
    )

@application.route('/api/submitSubredditInfo', methods=['POST'])
def submitSubredditInfo():
    # Parse the incoming data
    incoming = request.get_json()
    subreddit_name = incoming["subredditName"]
    subreddit_keywords = incoming["subredditKeywords"]
    logged_in_user_id = incoming["id"]

    # Query the user to append subreddits and keywords to it.  
    user = User.query.get(logged_in_user_id)
    if user == None:
        return jsonify(message='User is not authorized.'), 401

    # Check if the subreddit exists or not.
    check_subreddit = subreddit_exists(subreddit_name)
    if check_subreddit == False:
        return jsonify(error=True), 404

    # Only create a new Subreddit instance if one doesn't exist in the database already.
    if Subreddit.query.filter(Subreddit.subreddit_name==subreddit_name).first() is None: 
        subreddit = Subreddit(subreddit_name)
        db.session.add(subreddit)
        update = 'false'
    else:
        subreddit = Subreddit.query.filter(Subreddit.subreddit_name==subreddit_name).first()
        update = 'true'
        
    # Create a monitor instance for each keyword.
    subreddit_keywords = subreddit_keywords.split(',') # create a list of keywords 
    subreddit_keywords_no_spaces = []
    for subreddit_keyword in subreddit_keywords:
        subreddit_keywords_no_spaces.append(subreddit_keyword.strip()) # remove leading and trailing white spaces from each keyword

    for kw in subreddit_keywords_no_spaces:
        # check if Keyword objects are in the database already
        if Keyword.query.filter_by(keyword=kw).first() is not None:
            keyword = Keyword.query.filter_by(keyword=kw).first()
        else: # create new Keyword objects
            keyword = Keyword(kw)
            db.session.add(keyword)

        # Create a monitor object for the current user, subreddit, and keyword.
        monitor = Monitor(user=user, subreddit=subreddit, keyword=keyword)
        db.session.add(monitor)

    db.session.commit()

    # Send all monitor objects related to the current user and subreddit
    monitors = Monitor.query.join(Monitor.user, Monitor.subreddit).filter(Monitor.user==user, Monitor.subreddit==subreddit).all()

    monitors_serialized = Monitor.serialize_list(monitors)

    return jsonify(
        monitors=monitors_serialized,
        update=update
    )
           
@application.route('/api/fetchSubredditsInfo', methods=['GET'])
def fetchSubredditsInfo():
    # Fetch the logged in user
    logged_in_user_id = request.args.get('id')
    user = User.query.get(logged_in_user_id)
    if user == None:
        return jsonify(message='User is not authorized.'), 401

    # Check if the user is monitoring any subreddits and keywords yet. Use join() to query a self-referential structure.
    curr_user_monitors = Monitor.query.join(Monitor.user).filter(Monitor.user==user).first()
    
    if curr_user_monitors is None:
        monitors = []
        monitors_serialized = []
    else: # the user is monitoring subreddit(s).
        monitors = Monitor.query.join(Monitor.user).filter(Monitor.user==user).all()
        monitors_serialized = Monitor.serialize_list(monitors)

    return jsonify(monitors=monitors_serialized)

@application.route('/api/deleteMonitoredSubreddit', methods=['DELETE'])
def deleteMonitoredSubreddit():
    # Parse the incoming data
    logged_in_user_id = request.args.get('id')
    subreddit_name = request.args.get('subredditName')

    # Fetch the current user
    user = User.query.get(logged_in_user_id) 
    if user == None:
        return jsonify(message='User is not authorized.'), 401

    # Fetch the Monitor instances that correspond to the logged in user and designated subreddit.
    subreddit = Subreddit.query.filter(Subreddit.subreddit_name==subreddit_name).first()
    subreddit_monitors = Monitor.query.join(Monitor.user, Monitor.subreddit).filter(Monitor.user==user, Monitor.subreddit==subreddit).all()    

    # Delete the monitor instances corresponding to the designated subreddit.
    for subreddit_monitor in subreddit_monitors:
        db.session.delete(subreddit_monitor)
        db.session.commit()

    # Delete the Subreddit instance if there are no more Monitor instances corresponding to it.
    if Monitor.query.join(Monitor.subreddit).filter(Monitor.subreddit==subreddit).first() is None:
        db.session.delete(subreddit)

        # Delete any Keyword instances if there are no more Subreddit instances corresponding to it.
        keywords = Keyword.query.all()
        for keyword in keywords:
            check_for_keyword_orphans(keyword)
    
    # Return the new list of monitors that corrrespond to the logged in user and their subreddits (that now no longer have the deleted subreddit).
    new_monitors = Monitor.query.join(Monitor.user).filter(Monitor.user==user).all()
    return jsonify(monitors = Monitor.serialize_list(new_monitors))

@application.route('/api/submitPhoneNumber', methods=['POST'])
def submitPhoneNumber():
    # Parse the incoming data
    incoming = request.get_json()
    logged_in_user_id = incoming['id']
    phone_number = incoming['phoneNumber']

    # Format the phone number to be stored  in the database consistently.
    correctFormatPhoneNum = re.sub('[^0-9]', '', phone_number)

    # Place the phone number into the database.
    user = User.query.get(logged_in_user_id)
    if user == None:
        return jsonify(message='User is not authorized.'), 401
    user.phone_num = correctFormatPhoneNum

    try:
        db.session.commit()
    except Exception as e:
        return jsonify(message='This phone number is taken already.'), 409

    return jsonify(user.serialize())

@application.route('/api/deletePhoneNumber', methods=['DELETE'])
def deletePhoneNumber():
    # Parse the incoming data
    logged_in_user_id = request.args.get('id')    
    user = User.query.get(logged_in_user_id)
    if user == None:
        return jsonify(message='User is not authorized.'), 401

    user.phone_num = None # doesn't require .delete() since it's not a record, but a field within the record. A record is a whole row of a table.

    db.session.commit()

    return jsonify(user.serialize())



""" Helper Functions. """
def subreddit_exists(subreddit_name):
    # Create a reddit instance to use the Reddit API.
    reddit = praw.Reddit(client_id=Config.REDDIT_CLIENT_ID,
                        client_secret=Config.REDDIT_CLIENT_SECRET, password=Config.REDDIT_PASSWORD,
                        user_agent='Reddalerts 1.0 by u/boxcarcoder', username=Config.REDDIT_USERNAME)
    reddit.read_only = True

    # Check if the subreddit exists or not.
    exists = True
    try:
        reddit.subreddits.search_by_name(subreddit_name, exact=True)
    except NotFound:
        exists = False
    return exists       

def check_for_keyword_orphans(keyword):
    # check if each keyword has an associated subreddit
    if keyword.monitors == []:
        db.session.delete(keyword)
        db.session.commit()
        return True # keyword deleted
    else:
        return False # keyword has an associated subreddit


