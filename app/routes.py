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

    # Check if the user is monitoring this subreddit already. If they are, update the subreddit with keywords.
    if any(sr.subreddit_name == subreddit_name for sr in user.subreddits.all()): 
        for sr in user.subreddits:
            if sr.subreddit_name == subreddit_name:
                subreddit = sr

                # Create and add keyword instances to the subreddit instance
                subreddit_keywords = subreddit_keywords.split(',')
                for kw in subreddit_keywords:
                    keyword = Keyword(kw)
                    subreddit.keywords.append(keyword)

                db.session.commit()       

                return jsonify(
                    subreddit=subreddit.serialize(),
                    update='true'
                )    

    # If they aren't, create a new subreddit instance for the user.
    else:
        subreddit = Subreddit(subreddit_name)

        # Create and add keyword instances to the subreddit instance
        subreddit_keywords = subreddit_keywords.split(',')
        for kw in subreddit_keywords:
            keyword = Keyword(kw)
            subreddit.keywords.append(keyword)

        user.subreddits.append(subreddit)

        db.session.commit()

        return jsonify(
            subreddit=subreddit.serialize(),
            update='false'
        )    

@app.route('/api/fetchSubredditsInfo', methods=['GET'])
def fetchSubredditsInfo():
    # Fetch the logged in user
    logged_in_username = request.args.get('username')
    user = User.query.filter_by(username=logged_in_username).one()

    # Fetch the logged in user's subreddits
    subreddits = user.subreddits

    subreddits_serialized = Subreddit.serialize_list(subreddits)
    return jsonify(subreddits=subreddits_serialized)

@app.route('/api/deleteMonitoredSubreddit', methods=['DELETE'])
def deleteMonitoredSubreddit():
    # Parse the incoming data
    logged_in_user_id = request.args.get('id')
    subreddit_name = request.args.get('subredditName')

    # Remove the subreddit from the user
    user = User.query.get(logged_in_user_id) 
    subreddit = user.subreddits.filter_by(subreddit_name=subreddit_name).one()
    user.subreddits.remove(subreddit)
    db.session.commit()

    # Return the new list of subreddits
    return jsonify(subreddits = Subreddit.serialize_list(user.subreddits))

@app.route('/api/submitPhoneNumber', methods=['POST'])
def submitPhoneNumber():
    




