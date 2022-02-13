import streamlit as st

import utils.strategy as strategy
import utils.utils as utils


def app():
    st.title("Single Buy and Hold")
    target_stock = st.text_input("stock ticker", "SPY")
    years = st.slider('Select Year (starting from 01.01 end 12.31',
                      1990, 2021, value=(1991, 2020))
    monthly_money = st.text_input("monthly money", "1000")
    debt_ratio = st.text_input("init debt ratio", "0")

    result = strategy.single_buy_and_hold(target_stock, years=list(range(*years)), monthly_money=int(monthly_money),
                                          monthly_debt_ratio=float(debt_ratio))

    result2 = strategy.single_monthly_buy(target_stock, years=list(
        range(*years)), monthly_money=int(monthly_money))

    sell_years = f"{years[-1]}-12-31"

    st.subheader(
        f"buy and hold {result[-1].all_sell_profit_percent(sell_years)}")

    st.subheader(
        f"monthly buy {result2[-1].all_sell_profit_percent(sell_years)}")

    result = utils.result2df(result[1], [result[0], result2[0]], [
        "buy & hold", "monthly buy"])
    st.line_chart(data=result, width=0, height=0, use_container_width=True)
