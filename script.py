# import json
import praw
from config import Config
# import os
from twilio.rest import Client

# The Flask application
from app import app, db
from app.models import User, Subreddit, Keyword

"""
Creating the Flask instances for a shell context.
"""
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Subreddit': Subreddit, 'Keyword': Keyword}


# Create a reddit instance
reddit = praw.Reddit(client_id=Config.REDDIT_CLIENT_ID,
                     client_secret=Config.REDDIT_CLIENT_SECRET, password=Config.REDDIT_PASSWORD,
                     user_agent='Reddalerts 1.0 by u/boxcarcoder', username=Config.REDDIT_USERNAME)

reddit.read_only = True

# Create a twilio client
client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)

# Create test data to use with Praw and Twilio. This data will be received from the frontend as JSON.
decodedData = {}
decodedData["frugalmalefashion"] = [
    "Adidas", "North Face", "Patagonia"]


# Get rising posts that contain the user-designated keywords from the user-designated subreddit
userSubreddit = list(decodedData.keys())
userKeywords = list(decodedData.values())[0]

subreddit = reddit.subreddit(userSubreddit[0])

for submission in subreddit.rising():
    for keyword in userKeywords:
        if keyword in submission.title:
            # send the submission to a messaging api to send to the user

            # Make a POST request to the Programmable Messaging API's Message endpoint in order to create a new outbound message.
            # Use the twilio-python library's create() method.
            # message = client.messages \
            #     .create(
            #         body=submission.url,
            #         from_='+12058838200',
            #         to='+16263716944'
            #     )
            print('printing in place of texting.')
