import praw
import os
from dotenv import load_dotenv

class RedditClient:
    def __init__(self):
        load_dotenv()
        self.reddit = praw.Reddit(
            client_id=os.getenv('CLIENT_ID'),
            client_secret=os.getenv('CLIENT_SECRET'),
            user_agent="bookWorm"
        )
    
    def get_subreddit(self,name):
        return self.reddit.subreddit(name)