import streamlit as st
from utils.defaults import defaults
from utils.kantega import kantega_footer

defaults()

st.markdown("---")
col0, col1, col2 = st.columns(3)

with col0:
    st.empty()

with col1:
    st.markdown(
        "### [tinyurl.com/kantega-ai](https://adb-2582450973867059.19.azuredatabricks.net/login.html?o=2582450973867059) ",
        unsafe_allow_html=True,
    )
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/63/Databricks_Logo.png")
with col2:
    st.image("resources/image3.png", width=300)

kantega_footer()
