import time
from datetime import datetime

from twelvedata import TDClient

import yaml
import json

from twelvedata.exceptions import TwelveDataError


class stock_handler:
    stock_list = []
    td: TDClient

    def __init__(self):
        with open('resource.yaml', 'r') as f:
            data = yaml.safe_load(f)

        # Retrieve twelvedata stock api access data
        stock_api_data = data['stock_api_access_data']
        self.td = TDClient(apikey=stock_api_data["api_key"])

    def add_stock(self, stockpick):
        self.stock_list.append(stockpick)

    def get_stock_symbols(self):
        stock_data = list(self.td.get_stocks_list().as_json())
        stock_data = list(map(lambda data: data["symbol"], filter(lambda data: data["currency"] == "USD", stock_data)))
        with open("stock_data.json", "w") as write_file:
            json.dump(stock_data, write_file, indent=4)

    def get_stock_from_title(self, title: str) -> []:
        """
        Get the stock symbol from the title

        The title gets seperated by empty spaces.
        The split parts(entry) then get compared to a list containing all stock symbols.
        If the entry is in the list of Stocks, the entry gets

        :param title: the title that potentially has the symbol in it

        :return: the symbol that has been found in the string || if not found return empty string

        :test:
        * test 1:
        * test 2:
        """
        stock_json = open('stock_data.json', "r")
        stock_data = json.loads(stock_json.read())
        title = title.split(" ")
        stocks = []
        for entry in title:
            if entry.upper() in stock_data:
                stocks.append(entry.upper())
        return stocks

    def get_price_for_stocks(self, title: str):
        """
        get the price for all the stocks in the title

        get_stock_from_title is called to get all stocks form the title
        for each title the price is called through the api and when gotten added to a list with its symbol

        :param title: the title that potentially has the symbol in it

        :return: A List containing all prices and symbols in the title in json format

        :test:
        * test 1: title has no stock names
        * test 2: api calls exceeded
        """
        stocks = self.get_stock_from_title(title)
        prices = []
        for stock in stocks:
            prices.append(self.__get_price_for_stock(stock))
        return prices

    def __get_price_for_stock(self, stock: str):
        """
        Get the price for a singular stock("stock is assumed to be correct")

        The stock name is used to look up its current price,
        if that fails because the api usage limit has been reached,
        the programm waits until the minute is over and tries again

        :param stock: sybol(unique Name) for a stock

        :return: An Object containing the price and symbolname in json format

        :test:
        * test 1: api calls exceeded
        * test 2: stock name is wrong --> waisted api call
        """
        try:
            rp = self.td.price(
                symbol=stock
            )
            return {"symbol": stock, "price": rp.as_json()["price"]}
        except TwelveDataError:
            time.sleep(60 - datetime.utcnow().second)
            self.__get_price_for_stock(stock)
