"""
The Flask application object.
"""
from flask import Flask
from config import Config
from flask_cors import CORS

# Create the app module.
# __name__ is a Python predefined variable,
# which is set to the name of the module in which it is used.
application = Flask(__name__)

# Assign configurations to the application object.
application.config.from_object(Config)

# Allow CORS for all domains on all routes.
# Set supports_credentials to inject the Access-Control-Allow-Credentials header in responses.
CORS(application, supports_credentials=True)

# Allow requests only from my web app's domains or the development server.
application.config["CORS_ORIGIN"] = ["https://reddalerts.com", "https://www.reddalerts.com", "http://reddalerts.com", "http://www.reddalerts.com", "http://localhost:3000"]

# Import the public module which contains views.
# Import at the end to avoid circular import.
from app import public
