"""
The routes module for the Flask application.
"""
from flask import redirect, url_for
from flask_login import current_user, login_user
from app import app
from app.models import User


@app.route('/')
@app.route('/index')
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If the user is logged in already, redirect to the index page.
    if current_user.is_authenticated:
        return redirect(url_for('index'))


