from reddit_reader import RedditAPI
from thread import Thread
import json

def download_top_10000_posts_from_wallstreetbets():
    reddit_reader = RedditAPI()
    raw_dataset = reddit_reader.download_top_posts_of_all_time()
    print("Writing the dataset to file...")
    for dataset in raw_dataset:
        full_dataset = {
            "title": dataset.title,
            "gain_or_loss": dataset.gain_or_loss,
            "sentiment": "SAMPLE"
        }

        json_object = json.dumps(full_dataset)

        with open("sentiment_analysis_bot_dataset.json", "a") as outfile:
            outfile.write(json_object + "\n")
