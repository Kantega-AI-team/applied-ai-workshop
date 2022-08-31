import streamlit as st
from utils.background import add_bg_from_local
from utils.front_page import front_page


def defaults():
    st.set_page_config(
        layout="wide",
        page_title="Kunstig intelligens i praksis",
        page_icon="https://www.kantega.no/static/favicon.ico",
        initial_sidebar_state="collapsed",
    )
    add_bg_from_local("resources/image14.png")

    st.markdown(
        """
        <style>
    a:link, a:visited {
        color: #19254F;
        padding: 15px 25px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
    }

    a:hover, a:active {
        color: #EE3A64
    }
    </style>""",
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns([3, 1, 3, 3], gap="small")
    with col1:
        st.markdown("# [Kunstig intelligens i praksis](/)")
        st.markdown(
            "#### En kjapp innføring, konkrete eksempler, og hands-on arbeid med low code og åpne data"
        )
    with col2:
        st.markdown("")
    with col3:
        st.image("resources/image18.png", width=400)

    with col4:
        st.image("resources/echo.png")
