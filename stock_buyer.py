import datetime
import math

from database import Database
from stock_handler import StockHandler


class StockBuyer:
    money_available = 0
    database: Database
    stock_handler: StockHandler

    def __init__(self):
        self.database = Database()
        self.stock_handler = StockHandler()
        self.money_available = self.database.get_amount_in_bank()

    def buy_stocks(self, stocks: []):
        prices = self.stock_handler.get_price_for_stocks(stocks)
        for data in prices:
            price = float(data.get("price"))
            amount = 0
            if self.money_available > 1000:
                amount = 1000 // price
            else:
                amount = self.money_available // price
            if amount > 0:
                self.database.buy_stock(data.get("symbol"), amount, price)
                self.money_available = self.database.remove_from_bank(amount*price)

    def sell_stocks(self, stocks: []):
        prices = self.stock_handler.get_price_for_stocks(stocks)
        for data in prices:
            stock = data.get("symbol")
            price = float(data.get("price"))
            if self.database.do_we_own_stock(stock):
                to_sell_amount = self.database.get_stock_amount_owned(stock)
                self.database.sell_stock(data.get("symbol"), to_sell_amount, price)
                self.money_available = self.database.remove_from_bank(to_sell_amount*price*-1)
