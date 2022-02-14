import streamlit as st

import utils.strategy as strategy
import utils.utils as utils

import seaborn as sns
import matplotlib.pyplot as plt

import joblib

import utils.strategy_util as su
import itertools

import plotly.graph_objects as go
import numpy as np


def df_to_plotly(df):
    return {'z': df.values.tolist(),
            'x': df.columns.tolist(),
            'y': df.index.tolist()}


def app():
    st.title("Day Heatmap")
    target_stock = st.text_input("stock ticker", "SPY")
    # years = st.slider('Select Year (starting from 01.01 end 12.31',
    #                   1990, 2021, value=(1991, 2020))
    monthly_money = st.text_input("monthly money", "1000")
    debt_ratio = st.text_input("init debt ratio", "0")

    START_YEAR = 1993
    END_YEAR = 2021
    PERIOD = int(st.text_input("period", "20"))
    year_iters = su.period_year_iter(START_YEAR, END_YEAR-PERIOD, PERIOD)
    day_range = list(range(1, 28))

    iters = list(itertools.product(*[year_iters, day_range]))

    def new_func(x):
        years, day = x
        sell_years = f"{years[-1]}-12-31"
        return strategy.single_buy_and_hold(target_stock, years=years, monthly_money=int(monthly_money),
                                            monthly_debt_ratio=float(debt_ratio), buy_day=day)[-1].all_sell_profit_percent(sell_years)[target_stock]
    open_buy_hold = joblib.Parallel(n_jobs=8)(joblib.delayed(new_func)(x)
                                              for x in iters)

    close_buy_hold = []

    def new_func2(x):
        years, day = x
        sell_years = f"{years[-1]}-12-31"
        return strategy.single_buy_and_hold(target_stock, years=years, monthly_money=int(monthly_money),
                                            monthly_debt_ratio=float(debt_ratio), buy_day=day, col_ind="Close")[-1].all_sell_profit_percent(sell_years)[target_stock]
    close_buy_hold = joblib.Parallel(n_jobs=8)(joblib.delayed(new_func2)(x)
                                               for x in iters)

    result = utils.result2df(list(range(len(open_buy_hold))), [open_buy_hold, close_buy_hold], [
        "open buy_hold", "close buy_hold"])

    st.line_chart(data=result, width=0, height=0, use_container_width=True)

    dd = su.year_date_df(open_buy_hold, iters)
    fig = go.Figure(data=go.Heatmap(df_to_plotly(
        dd.pivot("start_year", "date", "earns"))))
    st.plotly_chart(fig, use_container_width=True)

    dd = su.year_date_df(close_buy_hold, iters)
    fig = go.Figure(data=go.Heatmap(df_to_plotly(
        dd.pivot("start_year", "date", "earns"))))
    st.plotly_chart(fig, use_container_width=True)

    def new_func(x):
        years, day = x
        sell_years = f"{years[-1]}-12-31"
        return strategy.single_monthly_buy(target_stock, years=years, monthly_money=int(monthly_money),
                                           buy_day=day)[-1].all_sell_profit_percent(sell_years)[target_stock]
    open_buy_hold = joblib.Parallel(n_jobs=8)(joblib.delayed(new_func)(x)
                                              for x in iters)

    def new_func2(x):
        years, day = x
        sell_years = f"{years[-1]}-12-31"
        return strategy.single_monthly_buy(target_stock, years=years, monthly_money=int(monthly_money),
                                           buy_day=day, col_ind="Close")[-1].all_sell_profit_percent(sell_years)[target_stock]
    close_buy_hold = joblib.Parallel(n_jobs=8)(joblib.delayed(new_func2)(x)
                                               for x in iters)

    result = utils.result2df(list(range(len(open_buy_hold))), [open_buy_hold, close_buy_hold], [
        "open monthly", "close monthly"])

    st.line_chart(data=result, width=0, height=0, use_container_width=True)

    dd = su.year_date_df(open_buy_hold, iters)
    fig = go.Figure(data=go.Heatmap(df_to_plotly(
        dd.pivot("start_year", "date", "earns"))))
    st.plotly_chart(fig, use_container_width=True)

    dd = su.year_date_df(close_buy_hold, iters)
    fig = go.Figure(data=go.Heatmap(df_to_plotly(
        dd.pivot("start_year", "date", "earns"))))
    st.plotly_chart(fig, use_container_width=True)
