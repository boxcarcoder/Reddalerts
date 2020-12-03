from flask import Flask

# Create an application object as an instance of class Flask.
# __name__ is a Python predefined variable, 
# which is set to the name of the module in which it is used.
app = Flask(__name__)

# The application imports modules, such as the routes module 
# from the app package (/app). The import is at the bottom as a 
# workaround to Flask's common problem with circular imports.
from app import routes