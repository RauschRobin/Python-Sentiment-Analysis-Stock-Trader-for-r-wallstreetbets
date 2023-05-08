from database import Database
from reddit_reader import RedditAPI
from sentiment_analysis_bot import SentimentAnalysisBot
from stock_buyer import StockBuyer
from stock_handler import StockHandler
from thread import Thread

def main():
    '''
    This function is the start of our program. When calling this function we scan the top posts of r/wallstreetbets and download them. We scan each post until we found enough stocks that we could buy. The sentiment analysis bot is calculating a sentiment for each post. Depending on the sentiment we vary the amount on how much we spend on each stock. When a stock is rated negative and we own that stock. We sell all of it, no matter how sure the sentiment analysis bot is. Each buy and sale is saved in a database.

    Parameters:
    None

    Returns:
    None
    '''
    # Call function that returns reddit threads
    counter = 0
    bought = 0
    amount_of_stocks_we_want_to_buy = 4 
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
        if sentiment_about_stock.sentiment == "positive" and bool(stocks) and sentiment_about_stock.accuracy >= 0.65:
            # Also simulate the stock and figure out it's chart
            stock_buyer.buy_stocks(stocks, sentiment_about_stock.accuracy)
            bought += 1
            if bought >= amount_of_stocks_we_want_to_buy:
                break
            print("Stock is good!")
            continue
        else:
            if bool(stocks):
                stock_buyer.sell_stocks(stocks)
            print("Stock is not worthy or couldn't be found!")
            continue


if __name__ == "__main__":
    main()
