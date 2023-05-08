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
        cursor = self.connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS stock_data(symbol TEXT PRIMARY KEY)")
        for symbol in data:
            response = cursor.execute("SELECT symbol FROM stock_data WHERE symbol == ?;", [symbol])
            value = response.fetchall()
            if not bool(value):
                cursor.execute("INSERT INTO stock_data ('symbol') VALUES (?);", [symbol])
        self.connection.commit()

    def get_stock_symbols(self):
        cursor = self.connection.cursor()
        response = cursor.execute("SELECT symbol FROM stock_data;")
        value = response.fetchall()
        return self.map_stock_symbols(value)

    def map_stock_symbols(self, symbols: []):
        mapped_symbol = []
        for symbol in symbols:
            mapped_symbol.append(symbol[0])
        return mapped_symbol

    def init_bank(self):
        cursor = self.connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS bank(amount double)")
        response = cursor.execute("SELECT amount FROM bank")
        value = response.fetchall()
        if not bool(value):
            cursor.execute("INSERT INTO bank ('amount') VALUES (?);", [100000])
            self.connection.commit()

    def get_amount_in_bank(self):
        cursor = self.connection.cursor()
        response = cursor.execute("SELECT amount FROM bank")
        value = response.fetchall()
        return value[0][0]

    def remove_from_bank(self, amount):
        current_available = self.get_amount_in_bank()
        cursor = self.connection.cursor()
        cursor.execute("UPDATE bank SET amount = ?", [current_available - amount])
        self.connection.commit()
        return self.get_amount_in_bank()

    def init_stocks_log(self):
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
        self._insert_into_stock_log(symbol, amount, price, True)

    def sell_stock(self, symbol, amount, price):
        print("trying to sell stock " + str(symbol) + " " + str(amount) + " " + str(price))
        self._insert_into_stock_log(symbol, amount, price, False)

    def _insert_into_stock_log(self, symbol, amount, price, buy):
        cursor = self.connection.cursor()
        values = (symbol, amount, price, buy)
        cursor.execute(
            "INSERT INTO stock_log (symbol, amount, price, buy) VALUES (?,?,?,?)",
            values
        )
        self.connection.commit()

    def get_stock_amount_owned(self, symbol):
        amount = 0
        stocks = self._get_stock_from_stock_log(symbol)
        for stock in stocks:
            if stock[3] == 1:
                amount += stock[1]
            else:
                amount -= stock[1]
        return amount

    def _get_stock_from_stock_log(self, symbol):
        cursor = self.connection.cursor()
        response = cursor.execute("SELECT * FROM stock_log WHERE symbol = ? ", [symbol])
        return response.fetchall()

    def do_we_own_stock(self, symbol):
        return self.get_stock_amount_owned(symbol) > 0

    def get_stock_log(self):
        cursor = self.connection.cursor()
        response = cursor.execute("SELECT * FROM stock_log ")
        return response.fetchall()
