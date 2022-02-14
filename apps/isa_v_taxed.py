import streamlit as st

import utils.strategy as strategy

import joblib

import utils.strategy_util as su

import plotly.graph_objects as go
from utils.div_data import data as div_data


def df_to_plotly(df):
    return {'z': df.values.tolist(),
            'x': df.columns.tolist(),
            'y': df.index.tolist()}


TAX_TYPE = {
    "US": (2500, 2000),
    "KR": (0, 2000000)
}


def app():
    st.title("ISA vs TAXED Heatmap - monthly buy")
    target_stock = st.text_input("stock ticker", "SPY")
    # years = st.slider('Select Year (starting from 01.01 end 12.31',
    #                   1990, 2021, value=(1991, 2020))
    monthly_money = st.text_input("monthly money", "1000")
    debt_ratio = st.text_input("init debt ratio", "0")

    START_YEAR = 1993
    END_YEAR = 2021
    tax_type = st.radio("Country", ('US', 'KR'))
    buy_type = st.radio("Buy_Type", ('Buy and Hold', 'Monthly'))

    div_mode = st.checkbox('dividend include')

    if div_mode:
        if not target_stock in div_data.keys():
            st.error(f"{target_stock} dividend info is missing")

    iters = []
    for p in range(1, 21):
        iters += su.period_year_iter(START_YEAR, END_YEAR-p, p)

    def tax_func(years):
        sell_years = f"{years[-1]}-12-31"
        if buy_type == "Buy and Hold":
            return strategy.single_buy_and_hold(target_stock, years=years, monthly_money=int(monthly_money),
                                                monthly_debt_ratio=float(debt_ratio), buy_day=1)[-1].all_sell_profit_percent(
                                                    sell_years, tax_free=TAX_TYPE[tax_type][0], tax_ratio=0.154)[target_stock]
        else:
            return strategy.single_monthly_buy(target_stock, years=years, monthly_money=int(monthly_money), buy_day=1)[-1].all_sell_profit_percent(
                sell_years, tax_free=TAX_TYPE[tax_type][0], tax_ratio=0.154)[target_stock]

    def isa_func(years):
        sell_years = f"{years[-1]}-12-31"
        if buy_type == "Buy and Hold":
            return strategy.single_buy_and_hold(target_stock, years=years, monthly_money=int(monthly_money),
                                                monthly_debt_ratio=float(debt_ratio), buy_day=1)[-1].all_sell_profit_percent(
                                                    sell_years, tax_free=TAX_TYPE[tax_type][1], tax_ratio=0.09)[target_stock]
        else:
            return strategy.single_monthly_buy(target_stock, years=years, monthly_money=int(monthly_money), buy_day=1)[-1].all_sell_profit_percent(
                sell_years, tax_free=TAX_TYPE[tax_type][1], tax_ratio=0.09)[target_stock]

    taxed = joblib.Parallel(n_jobs=8)(joblib.delayed(tax_func)(x)
                                      for x in iters)

    isaed = joblib.Parallel(n_jobs=8)(joblib.delayed(isa_func)(x)
                                      for x in iters)

    st.subheader("TAX returns")
    dd = su.year_df(taxed, iters)
    fig = go.Figure(data=go.Heatmap(df_to_plotly(
        dd.pivot("start_year", "invest_length", "earns"))))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("ISA returns")
    dd = su.year_df(isaed, iters)
    fig = go.Figure(data=go.Heatmap(df_to_plotly(
        dd.pivot("start_year", "invest_length", "earns"))))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("TAX vs ISA returns (+ TAX, - ISA)")
    dd = su.year_df(taxed, iters)
    dd2 = su.year_df(isaed, iters)
    dd3 = dd.pivot("start_year", "invest_length", "earns") - \
        dd2.pivot("start_year", "invest_length", "earns")
    fig = go.Figure(data=go.Heatmap(df_to_plotly(dd3)))
    st.plotly_chart(fig, use_container_width=True)

    if div_mode:
        def tax_func(years):
            sell_years = f"{years[-1]}-12-31"
            if buy_type == "Buy and Hold":
                return strategy.single_buy_and_hold(target_stock, years=years, monthly_money=int(monthly_money),
                                                    monthly_debt_ratio=float(debt_ratio), buy_day=1, add_div=True)[-1].all_sell_profit_percent(
                                                        sell_years, tax_free=TAX_TYPE[tax_type][0]*len(years), tax_ratio=0.154)[target_stock]
            else:
                return strategy.single_monthly_buy(target_stock, years=years, monthly_money=int(monthly_money), buy_day=1, add_div=True)[-1].all_sell_profit_percent(
                    sell_years, tax_free=TAX_TYPE[tax_type][0]*len(years), tax_ratio=0.154)[target_stock]

        def isa_func(years):
            sell_years = f"{years[-1]}-12-31"
            if buy_type == "Buy and Hold":
                return strategy.single_buy_and_hold(target_stock, years=years, monthly_money=int(monthly_money),
                                                    monthly_debt_ratio=float(debt_ratio), buy_day=1, add_div=True, tax_type="ISA")[-1].all_sell_profit_percent(
                                                        sell_years, tax_free=TAX_TYPE[tax_type][1], tax_ratio=0.09)[target_stock]
            else:
                return strategy.single_monthly_buy(target_stock, years=years, monthly_money=int(monthly_money), buy_day=1, add_div=True, tax_type="ISA")[-1].all_sell_profit_percent(
                    sell_years, tax_free=TAX_TYPE[tax_type][1], tax_ratio=0.09)[target_stock]

        taxed = joblib.Parallel(n_jobs=8)(joblib.delayed(tax_func)(x)
                                          for x in iters)

        isaed = joblib.Parallel(n_jobs=8)(joblib.delayed(isa_func)(x)
                                          for x in iters)
        st.subheader("div TAX returns")
        dd = su.year_df(taxed, iters)
        fig = go.Figure(data=go.Heatmap(df_to_plotly(
            dd.pivot("start_year", "invest_length", "earns"))))
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("div ISA returns")
        dd = su.year_df(isaed, iters)
        fig = go.Figure(data=go.Heatmap(df_to_plotly(
            dd.pivot("start_year", "invest_length", "earns"))))
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("div TAX vs ISA returns (+ TAX, - ISA)")
        dd = su.year_df(taxed, iters)
        dd2 = su.year_df(isaed, iters)
        dd3 = dd.pivot("start_year", "invest_length", "earns") - \
            dd2.pivot("start_year", "invest_length", "earns")
        fig = go.Figure(data=go.Heatmap(df_to_plotly(dd3)))
        st.plotly_chart(fig, use_container_width=True)

        def tax_func(years):
            sell_years = f"{years[-1]}-12-31"
            if buy_type == "Buy and Hold":
                return strategy.single_buy_and_hold(target_stock, years=years, monthly_money=int(monthly_money),
                                                    monthly_debt_ratio=float(debt_ratio), buy_day=1, add_div=True, reinvest=True)[-1].all_sell_profit_percent(
                                                        sell_years, tax_free=TAX_TYPE[tax_type][0]*len(years), tax_ratio=0.154)[target_stock]
            else:
                return strategy.single_monthly_buy(target_stock, years=years, monthly_money=int(monthly_money), buy_day=1, add_div=True, reinvest=True)[-1].all_sell_profit_percent(
                    sell_years, tax_free=TAX_TYPE[tax_type][0]*len(years), tax_ratio=0.154)[target_stock]

        def isa_func(years):
            sell_years = f"{years[-1]}-12-31"
            if buy_type == "Buy and Hold":
                return strategy.single_buy_and_hold(target_stock, years=years, monthly_money=int(monthly_money),
                                                    monthly_debt_ratio=float(debt_ratio), buy_day=1, add_div=True, tax_type="ISA", reinvest=True)[-1].all_sell_profit_percent(
                                                        sell_years, tax_free=TAX_TYPE[tax_type][1], tax_ratio=0.09)[target_stock]
            else:
                return strategy.single_monthly_buy(target_stock, years=years, monthly_money=int(monthly_money), buy_day=1, add_div=True, tax_type="ISA", reinvest=True)[-1].all_sell_profit_percent(
                    sell_years, tax_free=TAX_TYPE[tax_type][1], tax_ratio=0.09)[target_stock]

        taxed = joblib.Parallel(n_jobs=8)(joblib.delayed(tax_func)(x)
                                          for x in iters)

        isaed = joblib.Parallel(n_jobs=8)(joblib.delayed(isa_func)(x)
                                          for x in iters)
        st.subheader("div-re TAX returns")
        dd = su.year_df(taxed, iters)
        fig = go.Figure(data=go.Heatmap(df_to_plotly(
            dd.pivot("start_year", "invest_length", "earns"))))
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("div-re ISA returns")
        dd = su.year_df(isaed, iters)
        fig = go.Figure(data=go.Heatmap(df_to_plotly(
            dd.pivot("start_year", "invest_length", "earns"))))
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("div-re TAX vs ISA returns (+ TAX, - ISA)")
        dd = su.year_df(taxed, iters)
        dd2 = su.year_df(isaed, iters)
        dd3 = dd.pivot("start_year", "invest_length", "earns") - \
            dd2.pivot("start_year", "invest_length", "earns")
        fig = go.Figure(data=go.Heatmap(df_to_plotly(dd3)))
        st.plotly_chart(fig, use_container_width=True)

        def tax_func(years):
            sell_years = f"{years[-1]}-12-31"
            if buy_type == "Buy and Hold":
                return strategy.single_buy_and_hold(target_stock, years=years, monthly_money=int(monthly_money),
                                                    monthly_debt_ratio=float(debt_ratio), buy_day=1, add_div=True)[-1].all_sell_profit_percent(
                                                        sell_years, tax_free=TAX_TYPE[tax_type][0]*len(years), tax_ratio=0.154)[target_stock]
            else:
                return strategy.single_monthly_buy(target_stock, years=years, monthly_money=int(monthly_money), buy_day=1, add_div=True)[-1].all_sell_profit_percent(
                    sell_years, tax_free=TAX_TYPE[tax_type][0]*len(years), tax_ratio=0.154)[target_stock]

        def isa_func(years):
            sell_years = f"{years[-1]}-12-31"
            if buy_type == "Buy and Hold":
                return strategy.single_buy_and_hold(target_stock, years=years, monthly_money=int(monthly_money),
                                                    monthly_debt_ratio=float(debt_ratio), buy_day=1, add_div=True, tax_type="ISA")[-1].all_sell_profit_percent(
                                                        sell_years, tax_free=TAX_TYPE[tax_type][1], tax_ratio=0.09, add_benefit=408000)[target_stock]
            else:
                return strategy.single_monthly_buy(target_stock, years=years, monthly_money=int(monthly_money), buy_day=1, add_div=True, tax_type="ISA")[-1].all_sell_profit_percent(
                    sell_years, tax_free=TAX_TYPE[tax_type][1], tax_ratio=0.09, add_benefit=408000)[target_stock]

        taxed = joblib.Parallel(n_jobs=8)(joblib.delayed(tax_func)(x)
                                          for x in iters)

        isaed = joblib.Parallel(n_jobs=8)(joblib.delayed(isa_func)(x)
                                          for x in iters)
        st.subheader("div TAX returns")
        dd = su.year_df(taxed, iters)
        fig = go.Figure(data=go.Heatmap(df_to_plotly(
            dd.pivot("start_year", "invest_length", "earns"))))
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("div+Benefit ISA returns")
        dd = su.year_df(isaed, iters)
        fig = go.Figure(data=go.Heatmap(df_to_plotly(
            dd.pivot("start_year", "invest_length", "earns"))))
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("div+Benefit TAX vs ISA returns (+ TAX, - ISA)")
        dd = su.year_df(taxed, iters)
        dd2 = su.year_df(isaed, iters)
        dd3 = dd.pivot("start_year", "invest_length", "earns") - \
            dd2.pivot("start_year", "invest_length", "earns")
        fig = go.Figure(data=go.Heatmap(df_to_plotly(dd3)))
        st.plotly_chart(fig, use_container_width=True)

        def tax_func(years):
            sell_years = f"{years[-1]}-12-31"
            if buy_type == "Buy and Hold":
                return strategy.single_buy_and_hold(target_stock, years=years, monthly_money=int(monthly_money),
                                                    monthly_debt_ratio=float(debt_ratio), buy_day=1, add_div=True, reinvest=True)[-1].all_sell_profit_percent(
                                                        sell_years, tax_free=TAX_TYPE[tax_type][0]*len(years), tax_ratio=0.154)[target_stock]
            else:
                return strategy.single_monthly_buy(target_stock, years=years, monthly_money=int(monthly_money), buy_day=1, add_div=True, reinvest=True)[-1].all_sell_profit_percent(
                    sell_years, tax_free=TAX_TYPE[tax_type][0]*len(years), tax_ratio=0.154)[target_stock]

        def isa_func(years):
            sell_years = f"{years[-1]}-12-31"
            if buy_type == "Buy and Hold":
                return strategy.single_buy_and_hold(target_stock, years=years, monthly_money=int(monthly_money),
                                                    monthly_debt_ratio=float(debt_ratio), buy_day=1, add_div=True, tax_type="ISA", reinvest=True)[-1].all_sell_profit_percent(
                                                        sell_years, tax_free=TAX_TYPE[tax_type][1], tax_ratio=0.09, add_benefit=408000)[target_stock]
            else:
                return strategy.single_monthly_buy(target_stock, years=years, monthly_money=int(monthly_money), buy_day=1, add_div=True, tax_type="ISA", reinvest=True)[-1].all_sell_profit_percent(
                    sell_years, tax_free=TAX_TYPE[tax_type][1], tax_ratio=0.09, add_benefit=408000)[target_stock]

        taxed = joblib.Parallel(n_jobs=8)(joblib.delayed(tax_func)(x)
                                          for x in iters)

        isaed = joblib.Parallel(n_jobs=8)(joblib.delayed(isa_func)(x)
                                          for x in iters)
        st.subheader("div-re TAX returns")
        dd = su.year_df(taxed, iters)
        fig = go.Figure(data=go.Heatmap(df_to_plotly(
            dd.pivot("start_year", "invest_length", "earns"))))
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("div-re+Benefit ISA returns")
        dd = su.year_df(isaed, iters)
        fig = go.Figure(data=go.Heatmap(df_to_plotly(
            dd.pivot("start_year", "invest_length", "earns"))))
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("div-re+Benefit TAX vs ISA returns (+ TAX, - ISA)")
        dd = su.year_df(taxed, iters)
        dd2 = su.year_df(isaed, iters)
        dd3 = dd.pivot("start_year", "invest_length", "earns") - \
            dd2.pivot("start_year", "invest_length", "earns")
        fig = go.Figure(data=go.Heatmap(df_to_plotly(dd3)))
        st.plotly_chart(fig, use_container_width=True)
