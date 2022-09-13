import streamlit as st


def front_page():
    st.markdown("""---""")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            '<h2><a href="../Oversikt" target="_self">Oversikt</a></h2>',
            unsafe_allow_html=True,
        )
        st.markdown("En enkel innføring i hva kunstig intelligens egentlig er")
        st.markdown("\n", unsafe_allow_html=True)
        st.image("resources/hands.png")

    with col2:
        st.markdown(
            '<h2><a href="../Eksempler" target="_self">Eksempler</a></h2>',
            unsafe_allow_html=True,
        )
        st.markdown("Konkrete use case, inkludert et par fra Bergen")
        st.image("resources/muligheter.png")

    with col3:
        st.markdown(
            '<h2><a href="../Handson" target="_self">Hands on</a></h2>',
            unsafe_allow_html=True,
        )
        st.markdown("Vi blir småskitten på fingrene med litt low code ML i skyen")
        st.markdown("\n", unsafe_allow_html=True)
        st.image("resources/koder.png")
