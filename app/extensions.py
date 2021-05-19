"""
Additions to the Flask application object.
"""
from app.application import application
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler


# Initiate a DB instance using the SQLAlchemy Flask extension.
db = SQLAlchemy(application)

# Initiate a migration engine for the database using the Migrate Flask extension.
migrate = Migrate(application, db, render_as_batch=True)

# Initiate a background scheduler.
scheduler = BackgroundScheduler(daemon=True) 