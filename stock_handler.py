"""
author:
datum:
version:
license:
Modulkurzbeschreibung:
"""

import time
import os
from datetime import datetime

from twelvedata import TDClient

import yaml

from twelvedata.exceptions import TwelveDataError

from database import Database


class StockHandler:
    td: TDClient
    database: Database

    def __init__(self):
        """
        Initialise the StockHandler

        Initialise the Twelvedata td object and the Database

        :test:
        * test 1: Twelvedata api key not valid
        * test 2: Database is not initialised correctly
        * test 3: cant access the resource.yaml / stock_api_access_data
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))
        yaml_path = os.path.join(dir_path, 'resource.yaml')
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        # Retrieve twelvedata stock api access data
        stock_api_data = data['stock_api_access_data']
        self.td = TDClient(apikey=stock_api_data["api_key"])
        self.database = Database()

    def get_stock_symbols(self):
        """
        Get Stock symbols and insert them into the database

        Get all Stock symbols using USD as currency from the twelvedata api and insert them into the database

        :test:
        * test 1: Api Calls exceeded
        * test 2: Database already so it's trying to add already existing stock symbols
        """
        stock_data = list(self.td.get_stocks_list().as_json())
        stock_data = list(map(lambda data: data["symbol"], filter(lambda data: data["currency"] == "USD", stock_data)))
        self.database.init_stock_data(stock_data)

    def get_stock_from_title(self, title: str) -> []:
        """
        Get the stock symbol from the title

        The title gets seperated by empty spaces.
        The split parts(entry) then get compared to a list containing all stock symbols.
        If the entry is in the list of Stocks, the entry gets

        :param title: the title that potentially has the symbol in it

        :return: the symbol that has been found in the string || if not found return empty string

        :test:
        * test 1: The title contains words that aren't meant to be Stocks but are seen as such
        * test 2: The title contains stocks that can't be recognized, because the stock has been written wrong
        """
        stock_data = self.database.get_stock_symbols()
        title = title.split()
        stocks = []
        for entry in title:
            if entry.upper() in stock_data:
                stocks.append(entry.upper())
        return stocks

    def get_price_for_stocks(self, stocks: []):
        """
        get the price for all the stocks in the title

        get_stock_from_title is called to get all stocks form the title
        for each title the price is called through the api and when gotten added to a list with its symbol

        :param title: the title that potentially has the symbol in it

        :return: A List containing all prices and symbols in the title in json format

        :test:
        * test 1: stock names are not right
        * test 2: api calls exceeded
        """
        prices = []
        for stock in stocks:
            prices.append(self.__get_price_for_stock(stock, 0))
        return prices

    def __get_price_for_stock(self, stock: str, depth: int):
        """
        Get the price for a singular stock("stock is assumed to be correct")

        The stock name is used to look up its current price,
        if that fails because the api usage limit has been reached,
        the program waits until the minute is over and tries again

        :param stock: symbol(unique Name) for a stock

        :return: An Object containing the price and symbol name in json format

        :test:
        * test 1: api calls exceeded
        * test 2: stock name is wrong --> wasted api call
        """
        if depth >= 2:
            return None
        try:
            print(stock)
            rp = self.td.price(
                symbol=stock
            )
            return {"symbol": stock, "price": rp.as_json()["price"]}
        except TwelveDataError:
            print("sleepy")
            time.sleep(60 - datetime.utcnow().second)
            self.__get_price_for_stock(stock, depth + 1)
