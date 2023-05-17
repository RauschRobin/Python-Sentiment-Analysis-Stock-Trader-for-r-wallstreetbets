from datetime import datetime, timedelta
from database import Database
from stock_handler import StockHandler
import json

class ChartData:

    db = Database()
    stockHandler = StockHandler()
    def saveChart(self):
        """
        Function to save chart based on current Day

        Calculates the Worth of our available Stocks if available and adds it to out current bank amount

        :return: A static confirmation that the method has been executed

        * test 1: Cant get Stock price from Api because of limitations
        * test 2: Database not initialised
        * test 4: Can't get Price for the provided date
        """
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
                    value += amount * stock[2]
                    print("Exception occured for stock " + stock[0])

        self.db.insert_into_chart(date, bank+value)
        return {"value": "ausgefürt"}

    def getChart(self):
        """
        Function that return chart data

        Calls the Database function  get_chart

        :return: A list of tuples with the chart data

        :test:
        * test 1: Table does nto exist
        * test 2: Table is empty
        """
        return self.db.get_chart()