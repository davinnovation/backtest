import streamlit as st


class Pages:
    def __init__(self):
        self.pages = []

    def add_page(self, title, func) -> None:
        self.pages.append({
            "title": title,
            "function": func
        })

    def run(self):
        page = st.sidebar.selectbox(
            'Apps',
            self.pages,
            format_func=lambda page: page['title']
        )

        page['function']()
