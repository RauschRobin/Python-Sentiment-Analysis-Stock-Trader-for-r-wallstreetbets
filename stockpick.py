import datetime
import math

from database import Database
from stock_handler import StockHandler


class stockpick:
    stock_name = ""
    stock_name_short = ""
    price_buy = 0
    date_buy = datetime.now().timestamp()
    price_sell = 0
    date_sell = datetime.now().timestamp()
    amount = 0
    money_available = 0
    database: Database
    stock_handler: StockHandler

    def __init__(self, price_buy, amount, stock_name, stock_name_short):
        self.price_buy = price_buy
        self.amount = amount
        self.stock_name = stock_name
        self.stock_name_short = stock_name_short
        self.database = Database()
        self.stock_handler = StockHandler()
        self.money_available = self.database.get_amount_in_bank()

    def calculate_profit(price_buy, price_sell_or_current):
        profit = price_sell_or_current - price_buy
        return profit
    
    def set_price_sell_after_stock_is_sold(self, price_sold):
        self.price_sell = price_sold

    def buy_stock(self, stocks: []):
        for stock in stocks:
            price = self.stock_handler.get_price_for_stocks(stocks)
            amount = math.floor(1000 / price)
