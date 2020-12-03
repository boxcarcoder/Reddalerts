import praw
import config
import json
import os
from twilio.rest import Client

# The Flask application
from app import app

# Create a reddit instance
reddit = praw.Reddit(client_id=config.REDDIT_CLIENT_ID,
                     client_secret=config.REDDIT_CLIENT_SECRET, password=config.PASSWORD,
                     user_agent='Reddalerts 1.0 by u/boxcarcoder', username=config.USERNAME)

reddit.read_only = True

# Create a twilio client
client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)

# Create test data to use with Praw and Twilio. This data will be received from the frontend as JSON.
decodedData = {}
decodedData["frugalmalefashion"] = [
    "Adidas", "North Face", "Puma"]


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
            message = client.messages \
                .create(
                    body=submission.url,
                    from_='+12058838200',
                    to='+16263716944'
                )
