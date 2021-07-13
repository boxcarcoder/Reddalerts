import praw
from config import Config
from twilio.rest import Client

# The Flask application
from app.application import application
from app.extensions import db, scheduler
from app.models import User, Subreddit, Keyword

""" Create initial database designated by the DB URI, including all tables """
db.create_all()

""" Creating the Flask instances for a shell context. """
@application.shell_context_processor
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
def check_for_submissions(user, subreddit, monitored_keywords):
    for submission in subreddit.rising():
        for monitored_keyword in monitored_keywords:
            submissionTitleSplit = submission.title.split()
            if monitored_keyword.keyword in submissionTitleSplit and User.filter_by(received_posts=submission.title).one() is None:
                message = client.messages \
                    .create(
                        body=submission.url,
                        from_='+14256573687',
                        to='+1' + user.phone_num
                    )  
                user.received_posts.append(submission.title)                                                        #see if append() uses relation magic or not
                db.session.commit()       

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

""" Clear each user's queue (that stores what posts they've received already) after a day. """
def clear_submissions_queue():
    users = User.query.all()
    for user in users:
        user.received_posts = []    #*** i believe i can just set .received_posts to empty, as opposed to using .delete() since i am not deleting an entire row.
    db.session.commit()             #***
scheduler.add_job(clear_submissions_queue, 'interval', days=1)


""" Start the scheduler """
scheduler.start()


                # print('title: ', submission.title) 
                # print('keyword: ', monitored_keyword.keyword)
                # index = submission.title.index(monitored_keyword.keyword)
                # print('index: ', submission.title.index(monitored_keyword.keyword))
                # print('element at index: ', submission.title[index])
                # print('----------------------------------------')
                # Make a POST request to the Programmable Messaging API's Message endpoint in order to create a new outbound message.
                # Use the twilio-python library's create() method.
                # message = client.messages \
                #     .create(
                #         body=submission.url,
                #         from_='+' + user.phone_num,
                #         to='+16263716944'
                #     )    
                ##############