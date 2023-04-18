from database import Database
from reddit_reader import RedditAPI
from sentiment_analysis_bot import SentimentAnalysisBot
from stock_buyer import StockBuyer
from stock_handler import StockHandler
from thread import Thread


def main():
    # boolean IST EIN TEST UND MUSS NOCH ZU ZEIT ODER SO GEÄNDERT WERDEN!
    boolean = True
    while True:
        if boolean:
            boolean = False
            # Jonas:
            # Call function that returns reddit threads
            counter = 1
            reddit_handler = RedditAPI()
            stock_handler = StockHandler()
            stock_buyer = StockBuyer()
            while True:
                thread: Thread = reddit_handler.get_posts_of_day(counter)
                # Robin: 
                # Initialize Sentiment Anaylsis Bot
                sentiment_analysis_bot = SentimentAnalysisBot()
                # Figure out Sentiment of new Thread 
                sentiment_about_stock = sentiment_analysis_bot.run(thread.title, thread.gain_or_loss)

                # Ozan:
                # Figure out what stock is talked about and if we can buy it
                stocks: [] = stock_handler.get_stock_from_title(thread.title)
                if sentiment_about_stock == "positive" and bool(stocks):
                    # Also simulate the stock and figure out it's chart
                    stock_buyer.buy_stocks(stocks)
                    print("Stock is good")
                    break
                else:
                    # Thread ist scheiße wenn kein aktie herausgefunden wird oder kein gutes sentiment ist
                    # if(THREAD WAR SCHEISSE):
                    if bool(stocks):
                        stock_buyer.sell_stocks(stocks)
                    counter += 1
                    print("Stock is Shit")
                    continue

            # GRAFISCHE AUSGABE KOMMT NOCH


if __name__ == "__main__":
    main()
