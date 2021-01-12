"""
The routes module for the Flask application.
"""
from flask import redirect, url_for, request, jsonify
from flask_login import current_user, login_user
from app import app, db
from app.models import User, Subreddit, Keyword
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.exc import IntegrityError

@app.route('/')

@app.route('/index')

@app.route('/api/login', methods=['POST'])
def login():
    # Parse the incoming request
    incoming = request.get_json()
    email = incoming["email"]
    password = incoming["password"]

    # Check the database to see if the user exists. If successful, the route sends
    # a token back to the action, which stores the token into the redux state (reducer).

    # ** add a check for .one()
    user = User.query.filter_by(email=email).one()
    if user and user.check_password(password):
        # Generate a token for the user to send back to the frontend for authentication purposes.
        s = Serializer(app.config['SECRET_KEY'], expires_in=36000)
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

@app.route('/api/register', methods=['POST'])
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

    new_user = User.query.filter_by(email=incoming["email"]).one()

    # Generate a token for the new user to send back to the frontend for authentication purposes.
    s = Serializer(app.config['SECRET_KEY'], expires_in=36000)
    token = s.dumps({
        'id': new_user.id,
        'email': new_user.email,
    }).decode('utf-8')

    # Return the user to the frontend in order to populate the loggedInUser redux state.
    return jsonify(
        token=token,
        user=new_user.serialize()
    )

@app.route('/api/submitSubredditInfo', methods=['POST'])
def submitSubredditInfo():
    # Parse the incoming data
    incoming = request.get_json()
    subreddit_name = incoming["subredditName"]
    subreddit_keywords = incoming["subredditKeywords"]
    logged_in_username = incoming["username"]

    # Query the user to append subreddits and keywords to it.  
    user = User.query.filter_by(username=logged_in_username).one()

    # Create a subreddit instance to add to the DB
    subreddit = Subreddit(subreddit_name)

    # Create and add keyword instances to the subreddit instance
    subreddit_keywords = subreddit_keywords.split(',')
    for kw in subreddit_keywords:
        keyword = Keyword(kw)
        subreddit.keywords.append(keyword)

    # Add the subreddit instance to the user instance.
    user.subreddits.append(subreddit) 

    try:
        db.session.commit()
    except IntegrityError:
        return jsonify(message="User is monitoring this subreddit already."), 409

    #return the subreddit to the frontend.
    return jsonify(
        subreddit.serialize()
    )

@app.route('/api/fetchSubredditsInfo', methods=['GET'])
def fetchSubredditsInfo():
    # Fetch the logged in user
    logged_in_username = request.args.get('username')
    user = User.query.filter_by(username=logged_in_username).one()
    print('User who is fetching subreddits: ', user)

    # Fetch the logged in user's subreddits
    subreddits = user.subreddits

    subreddits_serialized = Subreddit.serialize_list(subreddits)
    return jsonify(subreddits=subreddits_serialized)