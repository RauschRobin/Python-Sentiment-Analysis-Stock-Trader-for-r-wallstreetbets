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

