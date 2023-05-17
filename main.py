from chart_data import ChartData
from reddit_reader import RedditAPI
from sentiment_analysis_bot import SentimentAnalysisBot
from stock_buyer import StockBuyer
from stock_handler import StockHandler
from thread import Thread
from fastapi import FastAPI

app = FastAPI()
chart = ChartData()

@app.get("/buy")
async def buy_stocks():
    """
    Function to buy stocks recommended by reddit

    In a Loop checks Reddit for the Top Posts of the Day,
    calculates the sentiment and buys if its positive and high enough

    :return: A static confirmation that the method has been executed

    :test:
    * test 1: api calls exceeded
    * test 2: Timeout on Request
    * test 3: Database not setup correctly
    * test 4: Stock / Price not found
    """
    # Call function that returns reddit threads
    counter = 0
    bought = 0
    amount_of_stocks_we_want_to_buy = 4 
    reddit_handler = RedditAPI()
    stock_handler = StockHandler()
    stock_buyer = StockBuyer()
    while True:
        thread: Thread = await reddit_handler.get_posts_of_day(counter)
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
        if sentiment_about_stock.sentiment == "positive" and bool(
                stocks) and sentiment_about_stock.accuracy >= 0.65:
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
    return {"value": "ausgefürt"}

@app.get("/saveChart")
async def save_chart_data():
    """
    Save chart_data endpoint

    In a Loop checks Reddit for the Top Posts of the Day,
    calculates the sentiment and buys if its positive and high enough

    :return: A static confirmation that the method has been executed

    :test:
    * test 1: api calls exceeded
    * test 2: Timeout on Request
    * test 3: Database not setup correctly
    * test 4: Stock / Price not found
    """
    return chart.saveChart()

@app.get("/getChart")
async def get_chart_data():
    """
    Function to buy stocks recommended by reddit

    In a Loop checks Reddit for the Top Posts of the Day,
    calculates the sentiment and buys if its positive and high enough

    :return: A static confirmation that the method has been executed

    :test:
    * test 1: api calls exceeded
    * test 2: Timeout on Request
    * test 3: Database not setup correctly
    * test 4: Stock / Price not found
    """
    return chart.getChart()
