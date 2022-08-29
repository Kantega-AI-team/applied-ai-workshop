from background import add_bg_from_local
from front_page import front_page
from overview import overview
from examples import examples
from kantega import kantega_footer

import streamlit as st

st.set_page_config(
    layout="wide",
    page_title="Kunstig intelligens i praksis",
    page_icon=":fire:",
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

page_names_to_funcs = {
    "Forside": front_page,
    "Oversikt": overview,
    "Eksempler": examples,
}

selected_page = st.sidebar.selectbox("Velg side", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

kantega_footer()
