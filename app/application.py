"""
The Flask application object.
"""
from flask import Flask
from config import Config

# Create an application object as an instance of class Flask.
# __name__ is a Python predefined variable,
# which is set to the name of the module in which it is used.
application = Flask(__name__)

# Assign configurations to the application object.
application.config.from_object(Config)