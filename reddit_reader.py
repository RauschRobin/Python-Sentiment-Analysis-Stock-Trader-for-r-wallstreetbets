import praw 

class Thread:
    def __init__(self, title, body, gain_or_loss):
        self.title = title
        self.body = body
        self.gain_or_loss = gain_or_loss

class RedditAPI:
    # Set up the Reddit API client
    def __init__(self):
        self.reddit = praw.Reddit(client_id='8FLiiST3e2FoD-iKhoQKAw',
                            client_secret='agWaeCM9Rdc1ziqQUbitJVeyDB0zZg',
                            user_agent='read wallstreetbets threads')

    # Retrieve a thread from r/wallstreetbets with the "Gain/Loss","day","top" filters + index(top to bottom)
    def get_post(self, index):
        subreddit = self.reddit.subreddit('wallstreetbets')
        posts = list(subreddit.search('flair:"Gain" OR flair:"Loss"', time_filter='day', sort='top', limit=index+1))
        if len(posts) >= index+1:
            top_post = posts[index]
            if top_post.link_flair_text == "Gain":
                return Thread(top_post.title, top_post.selftext, "gain")
            elif top_post.link_flair_text == "Loss":
                return Thread(top_post.title, top_post.selftext, "loss")
        else:
            return None
    
# Example usage
redditClient = RedditAPI()
thread = redditClient.get_post(0)
print(thread.__dict__)
thread = redditClient.get_post(1)
print(thread.__dict__)
thread = redditClient.get_post(2)
print(thread.__dict__)
thread = redditClient.get_post(3)
print(thread.__dict__)

