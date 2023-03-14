class stockpick:
    stock_name = ""
    stock_name_short = ""
    price_buy = 0
    amount = 0

    def __init__(self, price_buy, amount, stock_name, stock_name_short):
        self.price_buy = price_buy
        self.amount = amount
        self.stock_name = stock_name
        self.stock_name_short = stock_name_short

    def calculate_profit(price_buy, price_sell):
        profit = price_sell - price_buy
        return profit

