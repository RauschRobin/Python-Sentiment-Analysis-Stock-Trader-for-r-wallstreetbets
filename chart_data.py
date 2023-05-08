from datetime import datetime, timedelta
from database import Database
from stock_handler import StockHandler
import json

class ChartData:

    db = Database()
    stockHandler = StockHandler()
    date = datetime.now().date()
    def get_chart_data(self):
        response = {}
        stock_log = self.db.get_stock_log()
        self.date = datetime.strptime(stock_log[0][4], '%Y-%m-%d %H:%M:%S').date()
        one_day = timedelta(days=1)
        today = datetime.now().date()
        while today >= self.date:
            init_bank = 100000
            till_day_stocks = list(filter(self.is_before, stock_log))
            value = 0
            stock_amount = {}
            #Get how much money was spent?
            for stock in till_day_stocks:
                if stock[3] == 1:
                    if stock[0] in stock_amount:
                        stock_amount[stock[0]] += stock[1]
                    else:
                        stock_amount[stock[0]] = stock[1]
                    stock_amount[stock[0]] = stock[1]
                    value = value - stock[1] * stock[2]
                else:
                    stock_amount[stock[0]] -= stock[1]
                    value = value + stock[1] * stock[2]
            #Remove that amount from initial Bank
            init_bank += value
            for key, value in stock_amount.items():
                if value > 0:
                    price_string = str(self.stockHandler.get_stock_price_for_date(key, self.date))
                    price_string = price_string.replace("(", "[").replace(")", "]").replace("'", "\"")
                    # Parse the JSON list into a Python list of dictionaries
                    data = json.loads(price_string)
                    # Extract the 'high' and 'datetime' values from each dictionary using a list comprehension
                    price_date = [d['high'] for d in data]
                    init_bank += value * price_date
            response[self.date] = init_bank
            self.date = self.date + one_day

        return price_date

    def is_before(self, tuple):
        return datetime.strptime(tuple[4], '%Y-%m-%d %H:%M:%S').date() < self.date
