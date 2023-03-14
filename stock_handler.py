class stock_handler:
    stock_list = []

    def __init__(self):
        print("init stock handler")

    def add_stock(self, stockpick):
        self.stock_list.append(stockpick)
