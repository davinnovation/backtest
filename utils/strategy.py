from utils.backtest import BackTest
import utils.strategy_util as su
import utils.utils as utils

import functools


@functools.lru_cache(maxsize=32)
def load_data(stocks: tuple, stock_ids: tuple, start: str = "1990-01-01", end: str = "2022-02-01"):
    return utils.get_full_data(stocks, stock_ids, start, end)


def single_buy_and_hold(target_stock, years: list, monthly_money: int, monthly_debt_ratio: float = 0, col_ind="Open", buy_day=1):
    cur_money = []
    ind = []

    stock_data = load_data(tuple([target_stock]), tuple([target_stock]))

    bt = BackTest(stock_data)
    bt.buy(target_stock, monthly_money*len(years) *
           12, f"{years[0]}-01-{buy_day}", col_ind=col_ind)

    iters = su.year_month_day_iter(years, range(1, 13), [buy_day])

    for year, month, day in iters:
        bt.add_debt(monthly_money*len(years)*12 * monthly_debt_ratio/12)
        cur_money.append(bt.get_cur_price(f"{year}-{month}-{day}"))
        ind.append(f"{year}-{month}-{day}")
    return cur_money, ind, bt


def single_monthly_buy(target_stock, years: list, monthly_money: int, col_ind="Open", buy_day=1):
    cur_money = []
    ind = []
    stock_data = load_data(tuple([target_stock]), tuple([target_stock]))

    bt = BackTest(stock_data)

    iters = su.year_month_day_iter(years, range(1, 13), [buy_day])

    for year, month, day in iters:
        bt.buy(target_stock, monthly_money,
               f"{year}-{month}-{day}", col_ind=col_ind)
        cur_money.append(bt.get_cur_price(f"{year}-{month}-{day}"))
        ind.append(f"{year}-{month}-{day}")
    return cur_money, ind, bt
