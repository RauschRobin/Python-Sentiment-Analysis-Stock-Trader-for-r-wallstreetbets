from thread import Thread
import yaml
import praw
import os

class RedditAPI:
    # Set up the Reddit API client
    def __init__(self):
        '''
        Initializes the RedditAPI. This is the constructor. It loads the reddit api key and prepares praw to be used.

        Parameters:
        None

        Returns:
        None
        '''
        # Load the config file
        dir_path = os.path.dirname(os.path.realpath(__file__))
        yaml_path = os.path.join(dir_path, 'resource.yaml')
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)

        # Retrieve reddit api access data
        reddit_api_access_data = data['reddit_api_access_data']
        reddit_client_id = reddit_api_access_data['client_id']
        reddit_client_secret = reddit_api_access_data['client_secret']

        # Create reddit client
        self.reddit = praw.Reddit(client_id=reddit_client_id,
                            client_secret=reddit_client_secret,
                            user_agent='read wallstreetbets threads')

    # Retrieve a thread from r/wallstreetbets with the "day","top" filters + index(top to bottom)
    def get_posts_of_day(self, index):
        '''
        This functions returns the n'th post of the top posts of that day. You can set which top post you want by setting the parameter index.

        Parameters:
        index : int

        Returns:
        a new post: Thread object
        '''
        subreddit = self.reddit.subreddit('wallstreetbets')
        posts = list(subreddit.top(time_filter="day"))
        if len(posts) >= index+1:
            filtered_thread = posts[index]
            return Thread(filtered_thread.title)
        else:
            return None
        