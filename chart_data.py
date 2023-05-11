from datetime import datetime, timedelta
from database import Database
from stock_handler import StockHandler
import json

class ChartData:

    db = Database()
    stockHandler = StockHandler()
    def saveChart(self):
        response = {}
        date = datetime.now().date()
        stock_log = self.db.get_stock_log_grouped()
        bank = self.db.get_amount_in_bank()
        value = 0
        for stock in stock_log:
            amount = self.db.get_stock_amount_owned(stock[0])
            if amount > 0:
                try:
                    price_string = str(self.stockHandler.get_stock_price(stock[0]))
                    price_string = price_string.replace("(", "").replace(")", "").replace("'", "\"")[:-1]
                    # Parse the JSON list into a Python list of dictionaries
                    data = json.loads(price_string)
                    value += amount * float(data['high'])
                except:
                    print("Exception occured for stock " + stock[0])

        self.db.insert_into_chart(date, bank+value)
        return ""

    def getChart(self):
        return self.db.get_chart()