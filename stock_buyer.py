import datetime
import math

from database import Database
from stock_handler import StockHandler


class StockBuyer:
    money_available = 0
    database: Database
    stock_handler: StockHandler

    def __init__(self):
        """
        Initialise the StockBuyer

        Initialise the Database and the StockHandler

        :test:
        * test 1: StockHandler is not initialised correctly
        * test 2: Database is not initialised correctly
        * test 3 : Bank Table does not exist
        """
        self.database = Database()
        self.stock_handler = StockHandler()
        self.money_available = self.database.get_amount_in_bank()

    def buy_stocks(self, stocks: [], accuracyOnSentiment):
        """
        Buy the Stocks based on the Sentiments accuracy

        Get the Prices for all Stocks, then for each price and stock
        an amount is calculated based on the amount of money left in the Bank or 1000 Dollars,
        the price of a single stock and the SentimentAccuracy.
        If the amount is greater than 0.
        The System buy the set amount and reduces the amount left in the database.

        :param stocks: List of stock symbols to buy
        :param accuracyOnSentiment: accuracy of sentiment analysis bot between 0 and 1

        :test:
        * test 1: prices not found / Api Calls exceeded
        * test 2: data is not set
        * test 3: amount is not an integer but double/float
        * test 3: Bank not initialised
        * test 4: bought more than the budget allows because of the accuracyOnSentiment
        """
        prices = self.stock_handler.get_price_for_stocks(stocks)
        for data in prices:
            if data is None:
                continue
            price = float(data.get("price"))
            amount = 0
            if self.money_available > 1000:
                amount = int((1000 // price) * accuracyOnSentiment)
            else:
                amount = int((self.money_available // price) * accuracyOnSentiment)
            if amount > 0:
                self.database.buy_stock(data.get("symbol"), amount, price)
                self.money_available = self.database.remove_from_bank(amount*price)

    def sell_stocks(self, stocks: []):
        """
        Sell the Stocks

        Get the Prices for all Stocks, then for each price and stock
        we calculate the owned amount from the Database and Sell that in its entirety
        at the end we recalculate the amount in our bank

        :param stocks: List of stock symbols to sell

        :test:
        * test 1: prices not found / Api Calls exceeded
        * test 2: stock is not sold because price is not found
        * test 3: amount is calculated wrong, we sell more than we have
        """
        prices = self.stock_handler.get_price_for_stocks(stocks)
        for data in prices:
            if data is None:
                continue
            stock = data.get("symbol")
            price = float(data.get("price"))
            if self.database.do_we_own_stock(stock):
                to_sell_amount = self.database.get_stock_amount_owned(stock)
                self.database.sell_stock(data.get("symbol"), to_sell_amount, price)
                self.money_available = self.database.remove_from_bank(to_sell_amount*price*-1)
