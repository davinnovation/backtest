import FinanceDataReader as fdr
import pandas as pd


def get_full_data(stocks: list, stock_ids: list, start: str = "1990-01-01", end: str = "2022-02-01"):
    data = {}
    for i, stock in enumerate(stocks):
        data[stock_ids[i]] = fdr.DataReader(stock, start, end)

    return data


def result2df(index, data: list, data_name: list):
    df_plot = pd.DataFrame()
    for i, datum in enumerate(data):
        df_plot[data_name[i]] = datum
    df_plot.index = index
    return df_plot
