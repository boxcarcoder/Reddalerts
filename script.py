import praw
from config import Config
from twilio.rest import Client

# The Flask application
from app import app, db, scheduler
from app.models import User, Subreddit, Keyword

""" Creating the Flask instances for a shell context. """
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Subreddit': Subreddit, 'Keyword': Keyword}

""" Create a reddit instance. """
reddit = praw.Reddit(client_id=Config.REDDIT_CLIENT_ID,
                     client_secret=Config.REDDIT_CLIENT_SECRET, password=Config.REDDIT_PASSWORD,
                     user_agent='Reddalerts 1.0 by u/boxcarcoder', username=Config.REDDIT_USERNAME)

reddit.read_only = True

""" Create a twilio client. """
client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)

""" Periodically check for rising subreddits. """
# Check the retrieved subreddit's rising posts for any monitored keywords.
submissions_queue = []
def check_for_submissions(user, subreddit, monitored_keywords):
    for submission in subreddit.rising():
        for monitored_keyword in monitored_keywords:
            if monitored_keyword.keyword in submission.title and submission.title not in submissions_queue:
                # Make a POST request to the Programmable Messaging API's Message endpoint in order to create a new outbound message.
                # Use the twilio-python library's create() method.
                # message = client.messages \
                #     .create(
                #         body=submission.url,
                #         from_='+' + user.phone_num,
                #         to='+16263716944'
                #     )    
                ##############
                # message = client.messages \
                #     .create(
                #         body=submission.url,
                #         from_='+12058838200',
                #         to='+' + user.phone_num
                #     )   
                print('printing in place of texting.')
                submissions_queue.append(submission.title)

# Read all users in the database, and all of their subreddits and keywords.
def read_database():
    users = User.query.all()
    for user in users:
        monitored_subreddits = user.subreddits

        for monitored_subreddit in monitored_subreddits:
            monitored_keywords = monitored_subreddit.keywords
            subreddit = reddit.subreddit(monitored_subreddit.subreddit_name)
            check_for_submissions(user, subreddit, monitored_keywords)

scheduler.add_job(read_database, 'interval', minutes=1)

""" Clear submissions queue after a day """
def clear_submissions_queue():
    del submissions_queue[:]
scheduler.add_job(clear_submissions_queue, 'interval', days=1)


""" Start the scheduler """
scheduler.start()