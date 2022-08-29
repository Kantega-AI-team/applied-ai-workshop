import streamlit as st


def examples():
    st.markdown("# Eksempler")
    st.sidebar.markdown("# Eksempler")

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Diskriminerende redning",
            "Optimalisert bilplassering",
            "Telling med maskinsyn",
            "AI snooze?",
        ]
    )

    with tab1:
        st.header("Diskriminerende redning")

    with tab2:
        st.header("Optimalisert bilplassering")

    with tab3:
        st.header("Telling med maskinsyn")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
        st.camera_input("Take a picture")

    with tab4:
        st.header("AI snoozefunksjon ...eller?")
        img = st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
        print(img)
