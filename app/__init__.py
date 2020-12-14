"""
Module to create a Flask instance.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Create an application object as an instance of class Flask.
# __name__ is a Python predefined variable,
# which is set to the name of the module in which it is used.
app = Flask(__name__)

# Assign configurations to the application object.
app.config.from_object(Config)

# Initiate a DB instance using the SQLAlchemy Flask extension.
db = SQLAlchemy(app)

# Initiate a migration engine for the database using the Migrate Flask extension.
migrate = Migrate(app, db)

# The application imports modules, such as the routes module
# from the app package (/app). The import is at the bottom as a
# workaround to Flask's common problem with circular imports.
from app import routes, models

