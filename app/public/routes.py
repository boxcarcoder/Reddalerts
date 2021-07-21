"""
The routes module for the Flask application.
"""
from flask import request, jsonify, Response
from app.extensions import db
from app.application import application
from app.models import User, Subreddit, Keyword, Monitoring
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.exc import IntegrityError
import re

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

    # Begin monitoring the user and their subreddits and keywords.
    monitoring = Monitoring(user=user, subreddit=None, keyword=None)
    db.session.add(monitoring)
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

    # Check if the user is monitoring this subreddit already. If they are, update the monitoring instance with the keywords.

    # Fetch the user's monitoring status
    monitoring = Monitoring.query.filter(Monitoring.user.has(id=logged_in_user_id)).first()
    # print('==============')
    # print('monitoring in submitSubredditInfo: ', monitoring)
    # print('==============')
    
    # if Monitoring.query.filter_by(user=user, subreddit=subreddit_name).first() is not None:
    if monitoring.subreddit is not None:
        
        monitoring = Monitoring.query.filter_by(user=user, subreddit=subreddit_name).first()
        
        # Add keyword instances to the monitoring instance. Remove spaces too ***
        subreddit_keywords = subreddit_keywords.split(',')
        for kw in subreddit_keywords:
            # check if Keyword objects are in the database already
            if Keyword.query.filter_by(keyword=kw).first() is not None:
                keyword = Keyword.query.filter_by(keyword=kw).first()
            else: # create new Keyword objects
                keyword = Keyword(kw)            
            monitoring.keywords.append(keyword)

        db.session.commit()       

        return jsonify(
            subreddit=Monitoring.query.filter_by(users=user, subreddits=subreddit_name).serialize(),
            update='true'
        )    

    # If they aren't monitoring the subreddit yet, create a new subreddit instance and a new monitoring instance.
    else:
        subreddit = Subreddit(subreddit_name)
        
        # # Create a monitoring object which contains the unique relationship between User, Subreddit, and Keyword
        # monitoring = Monitoring(users=user, subreddits=subreddit)
        # # monitoring = Monitoring(users=user, subreddits=subreddit, keywords=subreddit_keywords[0])

        # Add the subreddit instance to the current logged in user's monitoring object.
        # monitoring = Monitoring.query.filter(Monitoring.users.has(id=logged_in_user_id)).first()

        monitoring = Monitoring.query.join(Monitoring.user, aliased=True).filter_by(id=logged_in_user_id).first()
        print('==============')
        print('monitoring in submitSubredditInfo: ', monitoring)
        print('==============')
        monitoring.subreddit = subreddit
        # monitoring.subreddit.append(subreddit)

        # Add keyword instances to the monitoring instance. Remove spaces too ***
        subreddit_keywords = subreddit_keywords.split(',')
        for kw in subreddit_keywords:
            # check if Keyword objects are in the database already
            if Keyword.query.filter_by(keyword=kw).first() is not None:
                keyword = Keyword.query.filter_by(keyword=kw).first()
            else: # create new Keyword objects
                keyword = Keyword(kw)
            
            if (monitoring.keyword is None):
                print('FUCK')
                monitoring.keyword = keyword
            else:
                print('YOU')
                monitoring.keyword.extend(keyword)

        # db.session.add(monitoring)
        db.session.commit()

        return jsonify(
            subreddit=subreddit.serialize(),
            update='false'
        )    

@application.route('/api/fetchSubredditsInfo', methods=['GET'])
def fetchSubredditsInfo():
    # Fetch the logged in user
    logged_in_user_id = request.args.get('id')
    user = User.query.get(logged_in_user_id)
    if user == None:
        return jsonify(message='User is not authorized.'), 401

    # Fetch the logged in user's subreddits
    monitoring = Monitoring.query.join(Monitoring.user, aliased=True).filter_by(id=logged_in_user_id).first()
    subreddits = monitoring.subreddit

    # Serialize and send the user's subreddits to the client.
    if subreddits is not None:
        subreddits_serialized = Subreddit.serialize_list(subreddits)
    else:
        subreddits_serialized = []
    return jsonify(subreddits=subreddits_serialized)

@application.route('/api/deleteMonitoredSubreddit', methods=['DELETE'])
def deleteMonitoredSubreddit():
    # Parse the incoming data
    logged_in_user_id = request.args.get('id')
    subreddit_name = request.args.get('subredditName')

    # Fetch the current user
    user = User.query.get(logged_in_user_id) 
    if user == None:
        return jsonify(message='User is not authorized.'), 401

    # Fetch the subreddit to be deleted.
    subreddit = Subreddit.query.filter_by(subreddit_name=subreddit_name).one()

    # Delete the monitored subreddit only if it no longer has an associated user.
    # How can I delete the subreddit since it is associated with the logged in user?
    # Remove the current user from the subreddit's list of users. I don't need to delete() the user, just remove the association.
    subreddits_without_curr_user = []
    for subreddit_user in subreddit.users:
        if (subreddit_user != user):
            subreddits_without_curr_user.append(subreddit_user)
    subreddit.users = subreddits_without_curr_user
   
    # Now that the subreddit is not associated with the logged in user, we can delete it if it is orphaned.
    check_for_subreddit_orphans(subreddit)

    # # Delete the monitored subreddit's keywords if the keywords no longer have an associated subreddit.
    # # Now that the subreddit is deleted (after disassociating with the logged in user), we can delete keywords if they're orphaned.
    # keywords = subreddit.keywords
    # for keyword in keywords:
    #     print('5')
    #     check_for_keyword_orphans(keyword)
    #     print('6')
    db.session.commit()

    # Return the new list of subreddits
    return jsonify(subreddits = Subreddit.serialize_list(user.subreddits))

@application.route('/api/submitPhoneNumber', methods=['POST'])
def submitPhoneNumber():
    # Parse the incoming data
    incoming = request.get_json()
    logged_in_user_id = incoming['id']
    phone_number = incoming['phoneNumber']

    # Format the phone number to be stored consistently.
    correctFormatPhoneNum = re.sub('[^0-9]', '', phone_number)

    # Place the phone number into the database.
    user = User.query.get(logged_in_user_id)
    if user == None:
        return jsonify(message='User is not authorized.'), 401
    user.phone_num = correctFormatPhoneNum

    db.session.commit()

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

def check_for_subreddit_orphans(subreddit):
    # check if each keyword has an associated user
    if len(subreddit.users) == 0:
        db.session.delete(subreddit)
        print('1')
        return True # subreddit deleted since it has no associated user
    else:
        print('2')
        return False # subreddit has an associated user


# def check_for_keyword_orphans(keyword):
#     # check if each keyword has an associated subreddit
#     if len(keyword.subreddits) == 0:
#         db.session.delete(keyword)
#         print('3')
#         return True # keyword deleted
#     else:
#         print('4')
#         return False # keyword has an associated subreddit





    # if any(sr.subreddit_name == subreddit_name for sr in user.subreddits.all()): 
    #     for sr in user.subreddits:
    #         if sr.subreddit_name == subreddit_name:
    #             subreddit = sr

    #             # Add keyword instances to the subreddit instance
    #             subreddit_keywords = subreddit_keywords.split(',')
    #             for kw in subreddit_keywords:
    #                 # check if Keyword objects are in the database already
    #                 if Keyword.query.filter_by(keyword=kw).first() is not None:
    #                     keyword = Keyword.query.filter_by(keyword=kw).first()
    #                     subreddit.keywords.append(keyword) 
    #                 else: # create new Keyword objects
    #                     keyword = Keyword(kw)
    #                     subreddit.keywords.append(keyword)

                # db.session.commit()       

                # return jsonify(
                #     subreddit=subreddit.serialize(),
                #     update='true'
                # )    