from thread import Thread
import yaml
import praw 
import time
from time import sleep
import prawcore

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
        posts = list(subreddit.search('flair:"Gain" OR flair:"Loss"', time_filter='day', sort='top', limit=index+1))
        if len(posts) >= index+1:
            filtered_thread = posts[index]
            if filtered_thread.link_flair_text == "Gain":
                return Thread(filtered_thread.title, "gain")
            elif filtered_thread.link_flair_text == "Loss":
                return Thread(filtered_thread.title, "loss")
        else:
            return None
        
    # Retrieve top 1000 posts of all time
    def download_top_posts_of_all_time(self):
        subreddit = self.reddit.subreddit('wallstreetbets')
        list_of_all_posts = []

        posts = None
        last_exception = None
        timeout = 1500 #seconds = 25 minutes
        time_start = int(time.time())
        while not posts and int(time.time()) < time_start + timeout:
            try:
                posts = list(subreddit.top(time_filter='all', limit=200))
            except prawcore.exceptions.ServerError as e:
                #wait for 30 seconds since sending more requests to overloaded server might not be helping
                last_exception = e
                print("calming the server down...")
                time.sleep(30)
        if not posts:
            raise last_exception

        #posts = list(subreddit.top(time_filter='all', limit=10000))
        for i in range(200):
            if len(posts) >= i+1:
                filtered_thread = posts[i]
                if filtered_thread.link_flair_text == "Gain":
                    list_of_all_posts.append(Thread(filtered_thread.title, "gain"))
                elif filtered_thread.link_flair_text == "Loss":
                    list_of_all_posts.append(Thread(filtered_thread.title, "loss"))
                else:
                    list_of_all_posts.append(Thread(filtered_thread.title, "other"))
            else:
                continue
        return list_of_all_posts