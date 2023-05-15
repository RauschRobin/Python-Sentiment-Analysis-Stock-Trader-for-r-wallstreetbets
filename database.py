import sqlite3
import os
from sqlite3 import Connection


class Database:
    connection: Connection

    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        db_path = os.path.join(dir_path, 'database')
        self.connection = sqlite3.connect(db_path)

    def init_stock_data(self, data: []):
        """
        Initialize stock_data Table in the Database with Symbol and add new entries

        If the Table stock_data does not exist we create a new Table with the Symbol as primary key
        Afterward we iterate through the data list.
        Check if the entry is already present in the Database.
        If not we insert the entry.

        :param data: List of StockSymbols

        :return: none

        :test:
        * test 1: entry is already in the Database
        * test 2: List contains non-Symbols
        """
        cursor = self.connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS stock_data(symbol TEXT PRIMARY KEY)")
        for symbol in data:
            response = cursor.execute("SELECT symbol FROM stock_data WHERE symbol == ?;", [symbol])
            value = response.fetchall()
            if not bool(value):
                cursor.execute("INSERT INTO stock_data ('symbol') VALUES (?);", [symbol])
        self.connection.commit()

    def get_stock_symbols(self):
        """
        Get the Stock symbols in the database

        Return all Symbols saved in the stock_data table

        :return: List of Stock symbols

        :test:
        * test 1: stock_data Table does not exist
        * test 2: stock_data is empty
        """
        cursor = self.connection.cursor()
        response = cursor.execute("SELECT symbol FROM stock_data;")
        value = response.fetchall()
        return self.map_stock_symbols(value)

    def map_stock_symbols(self, symbols: []):
        """
        Map table output to list of symbols

        Sqlite return the data as a tuple, so we map that to list containing only the data

        :param symbols: List of tuples

        :return: List of Stock symbols

        :test:
        * test 1: symbols is wrongly formatted
        * test 2: symbols contains non tuples
        """
        mapped_symbol = []
        for symbol in symbols:
            mapped_symbol.append(symbol[0])
        return mapped_symbol

    def init_bank(self):
        """
        Initialize bank Table in the Database with amount

        If the Table bank does not exist we create a new Table with the amount as a double.
        If there is no entry in the Table we Insert 10000 dollars into the database;

        :test:
        * test 1: There already is an entry
        * test 2: Table already exists
        """
        cursor = self.connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS bank(amount double)")
        response = cursor.execute("SELECT amount FROM bank")
        value = response.fetchall()
        if not bool(value):
            cursor.execute("INSERT INTO bank ('amount') VALUES (?);", [100000])
            self.connection.commit()

    def get_amount_in_bank(self):
        """
        Initialize bank Table in the Database with Symbol and add new entries

        If the Table stock_data does not exist we create a new Table with the Symbol as primary key

        :param data: List of StockSymbols

        :return: none

        :test:
        * test 1: entry is already in the Database
        * test 2: List contains non-Symbols
        """
        cursor = self.connection.cursor()
        response = cursor.execute("SELECT amount FROM bank")
        value = response.fetchall()
        return value[0][0]

    def remove_from_bank(self, amount):
        """
        Remove a certain amount from the Bank

        We Update the Value in the Database by remov-ing the given amount

        :test:
        * test 1: There are more than one entry
        * test 2: End amount is below 0 (in the negatives)
        """
        current_available = self.get_amount_in_bank()
        cursor = self.connection.cursor()
        cursor.execute("UPDATE bank SET amount = ?", [current_available - amount])
        self.connection.commit()
        return self.get_amount_in_bank()

    def init_stocks_log(self):
        """
        Initialize stock_log Table in the Database

        The stock_log is supposed to hold the Stock purchase and sale Data
        Containing the symbol, amount, current price, date and weather the action was a purchase.

        :test:
        * test 1: stock_data does not exist
        * test 2: Table already exists
        """
        cursor = self.connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS stock_log("
            "symbol text, "
            "amount double not null, "
            "price double not null, "
            "buy integer check (buy in (0, 1)) not null,"
            "date datetime default CURRENT_TIMESTAMP,"
            "foreign key (symbol) references stock_data(symbol))"
        )

    def buy_stock(self, symbol, amount, price):
        """
        Insert into stock_log a symbol with its amount and price that supposed to be bought

        The function calls the _insert_into_stock_log function.
        It's called in order to minimize errors with the buy or sell option

        :test:
        * test 1: symbol does not exist in stock_data
        * test 2: amount or price are in a different format
        """
        self._insert_into_stock_log(symbol, amount, price, True)

    def sell_stock(self, symbol, amount, price):
        """
        Insert into stock_log a symbol with its amount and price thats supposed to be sold

        The function calls the _insert_into_stock_log function.
        It's called in order to minimize errors with the buy or sell option

        :test:
        * test 1: symbol does not exist in stock_data
        * test 2: amount or price are in a different format
        """
        self._insert_into_stock_log(symbol, amount, price, False)

    def _insert_into_stock_log(self, symbol, amount, price, buy):
        """
        Insert into stock_log a symbol with its amount and price

        The function calls the _insert_into_stock_log function.
        It's called in order to minimize errors with the buy or sell option

        :test:
        * test 1: symbol does not exist in stock_data
        * test 2: amount or price are in a different format
        """
        cursor = self.connection.cursor()
        values = (symbol, amount, price, buy)
        cursor.execute(
            "INSERT INTO stock_log (symbol, amount, price, buy) VALUES (?,?,?,?)",
            values
        )
        self.connection.commit()

    def get_stock_amount_owned(self, symbol):
        """
        Get the amount of stocks owned my symbol

        The function gets all stocks_log information for a symbol
        Then adds the amount for those that have been bought and removes those that have been sold

        :test:
        * test 1: symbol does not exist in the stock_log
        * test 2: amount is negative
        """
        amount = 0
        stocks = self._get_stock_from_stock_log(symbol)
        for stock in stocks:
            if stock[3] == 1:
                amount += stock[1]
            else:
                amount -= stock[1]
        return amount

    def _get_stock_from_stock_log(self, symbol):
        """
        Get all entries from stock_log with the symbol

        The function gets all stocks_log information for a symbol
        Then adds the amount for those that have been bought and removes those that have been sold

        :test:
        * test 1: symbol does not exist in the stock_log
        * test 2: symbol is written wrong
        """
        cursor = self.connection.cursor()
        response = cursor.execute("SELECT * FROM stock_log WHERE symbol = ? ", [symbol])
        return response.fetchall()

    def do_we_own_stock(self, symbol):
        """
        Check if we currently have any of the stock available

        calls the get_stock_amount_owned function and checks if the value is greater then 0

        :test:
        * test 1: Amount owned is negative
        * test 2: symbol is written wrong or not in the stock_data
        """
        return self.get_stock_amount_owned(symbol) > 0
