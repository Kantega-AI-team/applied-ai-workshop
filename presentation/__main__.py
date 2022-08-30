import streamlit as st
from front_page import front_page
from utils.background import add_bg_from_local
from utils.kantega import kantega_footer

st.set_page_config(
    layout="wide",
    page_title="Kunstig intelligens i praksis",
    page_icon="https://www.kantega.no/static/favicon.ico",
    initial_sidebar_state="collapsed",
)
add_bg_from_local("resources/kantega.png")

streamlit_style = """
			<style>
			@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap');

			html, body, [class*="css"]  {
			font-family: 'Roboto', sans-serif;
			}
			</style>
			"""
st.markdown(streamlit_style, unsafe_allow_html=True)

front_page()
kantega_footer()
