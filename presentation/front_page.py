import streamlit as st


def front_page():
    st.markdown("# Kunstig intelligens i praksis")
    st.markdown(
        "#### En kjapp innføring, konkrete eksempler, og hands-on arbeid med low code og åpne data"
    )

    st.markdown("""---""")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("## Oversikt")

        st.markdown("En enkel innføring i hva kunstig intelligens egentlig er")
        st.markdown("\n", unsafe_allow_html=True)
        st.image("resources/hands.png")

    with col2:
        st.markdown("## Eksempler")
        st.markdown("Konkrete use case, inkludert et par fra Bergen")
        st.image("resources/muligheter.png")

    with col3:
        st.markdown("## Hands on")
        st.markdown("Vi blir småskitten på fingrene med litt low code ML i skyen")
        st.markdown("\n", unsafe_allow_html=True)
        st.image("resources/koder.png")
