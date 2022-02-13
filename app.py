import streamlit as st
import app_page
from apps import buy_and_hold, day_moving

app = app_page.Pages()

st.title("Stock App")
app.add_page("Buy and Hold", buy_and_hold.app)
app.add_page("Day Moving", day_moving.app)

app.run()
