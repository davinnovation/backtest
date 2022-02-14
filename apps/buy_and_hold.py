import streamlit as st

import utils.strategy as strategy
import utils.utils as utils
from utils.div_data import data as div_data

TAX_TYPE = {
    "US": (2500, 2000),
    "KR": (50000000, 2000000)
}


def app():
    st.title("Single Buy")
    target_stock = st.text_input("stock ticker", "SPY")
    years = st.slider('Select Year (starting from 01.01 end 12.31',
                      1990, 2021, value=(1993, 2021))
    monthly_money = st.text_input("monthly money", "1000")
    debt_ratio = st.slider('debt interest',
                           0., 1., value=0., step=0.005)

    tax_type = st.radio("Country", ('US', 'KR'))

    isa_mode = st.checkbox('ISA')
    div_mode = st.checkbox('dividend include')

    if div_mode:
        if not target_stock in div_data.keys():
            st.error(f"{target_stock} dividend info is missing")

    result = strategy.single_buy_and_hold(target_stock, years=list(range(*years)), monthly_money=int(monthly_money),
                                          monthly_debt_ratio=float(debt_ratio))

    result2 = strategy.single_monthly_buy(target_stock, years=list(
        range(*years)), monthly_money=int(monthly_money))

    sell_years = f"{years[-1]}-12-31"

    st.subheader(
        f"buy and hold {result[-1].all_sell_profit_percent(sell_years)}")

    st.subheader(
        f"monthly buy {result2[-1].all_sell_profit_percent(sell_years)}")

    st.subheader(
        f"taxed buy and hold {result[-1].all_sell_profit_percent(sell_years, tax_free=TAX_TYPE[tax_type][0]*len(years), tax_ratio=0.154)}")

    st.subheader(
        f"taxed monthly buy {result2[-1].all_sell_profit_percent(sell_years, tax_free=TAX_TYPE[tax_type][0]*len(years), tax_ratio=0.154)}")

    if isa_mode:
        st.subheader(
            f"isa buy and hold {result[-1].all_sell_profit_percent(sell_years, tax_free=TAX_TYPE[tax_type][1], tax_ratio=0.09)}")

        st.subheader(
            f"isa monthly buy {result2[-1].all_sell_profit_percent(sell_years, tax_free=TAX_TYPE[tax_type][1], tax_ratio=0.09)}")

    result = utils.result2df(result[1], [result[0], result2[0]], [
        f"buy & hold _ {debt_ratio}", "monthly buy"])
    st.line_chart(data=result, width=0, height=0, use_container_width=True)

    if div_mode:
        result = strategy.single_buy_and_hold(target_stock, years=list(range(*years)), monthly_money=int(monthly_money),
                                              monthly_debt_ratio=float(debt_ratio), add_div=True)

        result2 = strategy.single_monthly_buy(target_stock, years=list(
            range(*years)), monthly_money=int(monthly_money), add_div=True)

        st.subheader(
            f"taxed buy and hold {result[-1].all_sell_profit_percent(sell_years, tax_free=TAX_TYPE[tax_type][0]*len(years), tax_ratio=0.154)}")

        st.subheader(
            f"taxed monthly buy {result2[-1].all_sell_profit_percent(sell_years, tax_free=TAX_TYPE[tax_type][0]*len(years), tax_ratio=0.154)}")

        result = utils.result2df(result[1], [result[0], result2[0]], [
            f"buy & hold _ {debt_ratio} + div", "monthly buy + div"])
        st.line_chart(data=result, width=0, height=0, use_container_width=True)

        result = strategy.single_buy_and_hold(target_stock, years=list(range(*years)), monthly_money=int(monthly_money),
                                              monthly_debt_ratio=float(debt_ratio), tax_type="ISA")

        result2 = strategy.single_monthly_buy(target_stock, years=list(
            range(*years)), monthly_money=int(monthly_money), tax_type="ISA")
        st.subheader(
            f"isa buy and hold {result[-1].all_sell_profit_percent(sell_years, tax_free=TAX_TYPE[tax_type][1], tax_ratio=0.09)}")

        st.subheader(
            f"isa monthly buy {result2[-1].all_sell_profit_percent(sell_years, tax_free=TAX_TYPE[tax_type][1], tax_ratio=0.09)}")
