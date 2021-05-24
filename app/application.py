"""
The Flask application object.
"""
from flask import Flask
from config import Config


# Create the app module.
# __name__ is a Python predefined variable,
# which is set to the name of the module in which it is used.
application = Flask(__name__)

# Assign configurations to the application object.
application.config.from_object(Config)

# # Import routes at the end to avoid circular import.
# from app import public
