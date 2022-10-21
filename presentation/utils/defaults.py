import streamlit as st


def defaults():
    # Standard page config settings
    st.set_page_config(
        layout="wide",
        page_title="Kunstig intelligens i praksis",
        page_icon="https://www.kantega.no/static/favicon.ico",
        initial_sidebar_state="collapsed",
    )
    # Change url color
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

    st.markdown(
        """
                <style>
                @import url('https://fonts.googleapis.com/css2?family=Source Sans Pro:wght@100&display=swap');

                html, body, [class*="css"]  {
                font-family: 'Roboto', sans-serif;
                }
                </style>
                """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns([4, 1, 5, 4], gap="small")
    with col1:
        st.markdown(
            '<h2><a href="../" target="_self">Kunstig intelligens i praksis</a></h2>',
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown("")
    with col3:
        st.image("resources/Kantega_logo.png", width=400)

    with col4:
        st.markdown(
            "#### En kjapp innføring, konkrete eksempler, og hands-on arbeid med low code og åpne data"
        )
