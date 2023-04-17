from thread import Thread
import yaml
import praw 

class RedditAPI:
    # Set up the Reddit API client
    def __init__(self):
        # Load the config file 
        with open('resource.yaml', 'r') as f:
            data = yaml.safe_load(f)

        # Retrieve reddit api access data
        reddit_api_access_data = data['reddit_api_access_data']
        reddit_client_id = reddit_api_access_data['client_id']
        reddit_client_secret = reddit_api_access_data['client_secret']

        # Create reddit client
        self.reddit = praw.Reddit(client_id=reddit_client_id,
                            client_secret=reddit_client_secret,
                            user_agent='read wallstreetbets threads')

    # Retrieve a thread from r/wallstreetbets with the "Gain/Loss","day","top" filters + index(top to bottom)
    def get_posts_of_day(self, index):
        subreddit = self.reddit.subreddit('wallstreetbets')
        posts = list(subreddit.search('flair:"YOLO" OR flair:"Chart"', time_filter='day', sort='top', limit=index+1))
        if len(posts) >= index+1:
            filtered_thread = posts[index]
            if filtered_thread.link_flair_text == "YOLO":
                return Thread(filtered_thread.title, "yolo")
            elif filtered_thread.link_flair_text == "Chart":
                return Thread(filtered_thread.title, "chart")
        else:
            return None
        