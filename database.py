import sqlite3
from sqlite3 import Connection


class Database:
    connection: Connection

    def __init__(self):
        self.connection = sqlite3.connect("database")

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
        cursor.execute("SELECT amount FROM bank")
        response = cursor.execute("SELECT symbol FROM bank")
        value = response.fetchall()
        return value[0]

    def init_stocks_log(self):
        cursor = self.connection.cursor()
        cursor.execute(
        "CREATE TABLE IF NOT EXISTS stock_log("
        "symbol text, "
        "amount double not null, "
        "price double not null, "
        "sold INTEGER CHECK (sold IN (0, 1)) not null,"
        "foreign key (symbol) references stock_data(symbol))")

    def buy_stock(self):
        print("")

    def sell_stock(self):
        print("")