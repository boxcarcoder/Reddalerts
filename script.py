import praw
from config import Config
from twilio.rest import Client

# The Flask application
from app import app, db, scheduler
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

# Check the retrieved subreddit's rising posts for any monitored keywords.
submissionsQueue = []
def check_for_submissions(subreddit, monitored_keywords):
    for submission in subreddit.rising():
        for monitored_keyword in monitored_keywords:
            if monitored_keyword.keyword in submission.title and submission.title not in submissionsQueue:
                # Make a POST request to the Programmable Messaging API's Message endpoint in order to create a new outbound message.
                # Use the twilio-python library's create() method.
                # message = client.messages \
                #     .create(
                #         body=submission.url,
                #         from_='+12058838200',
                #         to='+16263716944'
                #     )    
                submissionsQueue.append(submission.title)
                print('printing in place of texting.')

# Read all users in the database, and all of their subreddits and keywords.
def read_database():
    users = User.query.all()
    for user in users:
        monitored_subreddits = user.subreddits

        for monitored_subreddit in monitored_subreddits:
            monitored_keywords = monitored_subreddit.keywords
            subreddit = reddit.subreddit(monitored_subreddit.subreddit_name)
            check_for_submissions(subreddit, monitored_keywords)

# Periodically check for rising subreddits.
scheduler.add_job(read_database, 'interval', minutes=1)
scheduler.start()




# # Create test data to use with Praw and Twilio. This data will be received from the frontend as JSON.
# decodedData = {}
# decodedData["frugalmalefashion"] = [
#     "Adidas", "North Face", "Patagonia"]

# # Get rising posts that contain the user-designated keywords from the user-designated subreddit
# userSubreddit = list(decodedData.keys())
# userKeywords = list(decodedData.values())[0]

# subreddit = reddit.subreddit(userSubreddit[0])

# for submission in subreddit.rising():
#     for keyword in userKeywords:
#         if keyword in submission.title:
#             # send the submission to a messaging api to send to the user

#             # Make a POST request to the Programmable Messaging API's Message endpoint in order to create a new outbound message.
#             # Use the twilio-python library's create() method.
#             # message = client.messages \
#             #     .create(
#             #         body=submission.url,
#             #         from_='+12058838200',
#             #         to='+16263716944'
#             #     )
#             print('printing in place of texting.')
