from database import Database
from reddit_reader import RedditAPI
from sentiment_analysis_bot import SentimentAnalysisBot
from stock_buyer import StockBuyer
from stock_handler import StockHandler
from thread import Thread


def main():
    # Call function that returns reddit threads
    counter = 0
    bought = 0
    reddit_handler = RedditAPI()
    stock_handler = StockHandler()
    stock_buyer = StockBuyer()
    while True:
        thread: Thread = reddit_handler.get_posts_of_day(counter)
        counter += 1
        print(counter)
        if thread is None:
            break
        # Initialize Sentiment Anaylsis Bot
        sentiment_analysis_bot = SentimentAnalysisBot()
        # Figure out Sentiment of new Thread
        sentiment_about_stock = sentiment_analysis_bot.run(thread.title)

        # Figure out what stock is talked about and if we can buy it
        stocks: [] = stock_handler.get_stock_from_title(thread.title)
        if sentiment_about_stock == "positive" and bool(stocks):
            # Also simulate the stock and figure out it's chart
            stock_buyer.buy_stocks(stocks)
            bought += 1
            if bought >= 4:
                break
            print("Stock is good")
            continue
        else:
            if bool(stocks):
                stock_buyer.sell_stocks(stocks)
            print("Stock is not worthy")
            continue


if __name__ == "__main__":
    main()
