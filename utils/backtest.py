class BackTest:
    def __init__(self, stock_data: dict):
        self.data = stock_data
        self.remained_money = 0
        self.hold = {}
        self.hold_price = {}

    def buy(self, stock, money, start_date, col_ind="Open", month_index=0):
        price = self.data[stock][self.data[stock].index >=
                                 start_date][col_ind][month_index]
        self.hold.setdefault(stock, 0)
        self.hold_price.setdefault(stock, 0)
        buy_count = int(money/price)
        self.hold_price[stock] = (
            self.hold[stock] * self.hold_price[stock] + buy_count * price)/(self.hold[stock]+buy_count)
        self.hold[stock] += buy_count
        self.remained_money += money - buy_count * price

    def get_cur_price(self, date, col_ind="Open"):
        cur_money = self.remained_money
        for key in self.hold.keys():
            stock = self.hold[key]
            cur_money += self.data[key][self.data[key].index >=
                                        date][col_ind][0] * stock
        return cur_money

    def add_debt(self, debt):
        self.remained_money -= debt

    def all_sell_profit(self, date, col_ind='Open'):
        profit = {}
        for key in self.hold.keys():
            stock = self.hold[key]
            cur_value = self.data[key][self.data[key].index >=
                                       date][col_ind][0] * stock
            profit[key] = cur_value - self.hold_price[key] * self.hold[key]
        return profit

    def all_sell_profit_percent(self, date, col_ind='Open'):
        profit = {}
        for key in self.hold.keys():
            stock = self.hold[key]
            cur_value = self.data[key][self.data[key].index >=
                                       date][col_ind][0] * stock
            profit[key] = cur_value - self.hold_price[key] * self.hold[key]
            profit[key] = profit[key]/(self.hold_price[key] * self.hold[key])
        return profit
