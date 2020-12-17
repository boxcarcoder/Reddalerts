"""
The routes module for the Flask application.
"""
from flask import redirect, url_for, request, jsonify
from flask_login import current_user, login_user
from app import app
from app.models import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@app.route('/')
@app.route('/index')
@app.route('/api/login', methods=['POST'])
def login():
    # If the user is logged in already, redirect to the index page.
    # if current_user.is_authenticated:

        # return redirect(url_for('index'))

    # Parse the incoming request
    incoming = request.get_json()
    email = incoming["email"]
    password = incoming["password"]

    # Check the database to see if the user exists. If successful, the route sends
    # a token back to the action, which stores the token into the redux state (reducer).
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        s = Serializer(app.config['SECRET_KEY'], expires_in=36000)
        token = s.dumps({
            'id': user.id,
            'email': user.email,
        }).decode('utf-8')
        return jsonify(token)

    # If the user doesn't exist
    return jsonify(error=True), 401





    


