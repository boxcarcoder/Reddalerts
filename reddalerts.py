import praw
from prawcore import NotFound
from config import Config
from twilio.rest import Client

# The Flask application
from app.application import application
from app.extensions import db, scheduler
from app.models import User, Subreddit, Keyword, Monitor, ReceivedPost

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
def check_for_submissions(user, subreddit, keyword):
    # Check the retrieved subreddit's rising posts for each monitored keyword.
    for submission in subreddit.rising():
        submissionTitleSplit = submission.title.split()

        if keyword.keyword in submissionTitleSplit and ReceivedPost.query.join(User).filter(User.username==user.username, ReceivedPost.received_post==submission.title).first() is None:    
            # client.messages \
            #     .create(
            #         body='"' + submission.title + '"' + '\n'+ submission.url,
            #         from_='+14256573687',
            #         to='+1' + user.phone_num
            #     )  
            print('##### SENDING NEWFOUND SUBMISSION.')

            # Prevent the same posts being sent to the user on repeat scans.
            received_post = ReceivedPost(submission.title)
            db.session.add(received_post)
            user.received_post.append(received_post)  
            db.session.commit()       

""" Read all users in the database, and all of their subreddits and keywords. """
def read_database():
    monitors = Monitor.query.all()
    for monitor in monitors:
        # User
        user = monitor.user
        # Subreddit
        subreddit = monitor.subreddit
        monitored_subreddit = reddit.subreddit(subreddit.subreddit_name)            
        # Keyword
        keyword = monitor.keyword        

        check_for_submissions(user, monitored_subreddit, keyword)

scheduler.add_job(read_database, 'interval', minutes=2)

""" Clear each user's received posts after a day. """
def clear_user_received_post():
    users = User.query.all()
    for user in users:
        for received_post in user.received_post:
            db.session.delete(received_post)
    db.session.commit()  

scheduler.add_job(clear_user_received_post, 'interval', days=1)




""" Start the scheduler """
scheduler.start()
