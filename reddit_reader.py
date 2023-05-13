from thread import Thread
import yaml
import praw
import os

class RedditAPI:
    # Set up the Reddit API client
    def __init__(self):
        """
        Initializes the Reddit API client.

        This method reads the configuration file and sets up the Reddit API client using the provided access data.

        param: None

        :return: None

        :test:
        * test 1: Instantiate the RedditAPIClient class and verify that the reddit attribute is initialized and is an instance of praw.Reddit. 
        * test 2: Simulate a missing or incorrect configuration file by either creating an empty configuration file or modifying an existing one. 
                  Instantiate the RedditAPIClient class and verify that the reddit attribute is not initialized. 
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))
        yaml_path = os.path.join(dir_path, 'resource.yaml')
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)

        reddit_api_access_data = data['reddit_api_access_data']
        reddit_client_id = reddit_api_access_data['client_id']
        reddit_client_secret = reddit_api_access_data['client_secret']

        self.reddit = praw.Reddit(client_id=reddit_client_id,
                            client_secret=reddit_client_secret,
                            user_agent='read wallstreetbets threads')

    def get_posts_of_day(self, index):
        """
        This functions returns the n'th post of the top posts of that day. You can set which top post you want by setting the parameter index.

        :param index: on what index to get the post

        :return: The title of the post in form of a Thread object

        :test:
        * test 1: Retrieve post on index 10 and check if return value is not none
        * test 2: Attempt to retrieve a post beyond the available posts for the day. Return value should be none
        """
        subreddit = self.reddit.subreddit('wallstreetbets')
        posts = list(subreddit.top(time_filter="day"))
        if len(posts) >= index+1:
            filtered_thread = posts[index]
            return Thread(filtered_thread.title)
        else:
            return None
        
