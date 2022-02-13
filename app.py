import streamlit as st
import app_page
from apps import buy_and_hold, day_moving

app = app_page.Pages()

app.add_page("Single Buy", buy_and_hold.app)
app.add_page("Day Moving", day_moving.app)

app.run()
