import streamlit as st


def kantega_footer():
    st.markdown("""---""")
    with st.expander("Hvem er det som snakker?"):

        col1, col2, col3 = st.columns(3, gap="large")

        with col1:
            st.image("resources/kantega_logo.png", width=200)
            st.markdown(
                """
            #### Vi som jobber i Kantega mener vi har verdens beste arbeidsplass. 
            Vi eier alle like mye og vi jobber alle mot et felles mål. 
            
            I tillegg får vi jobbe med fantastiske kunder og viktige prosjekter som betyr mye for mange.
            
            """
            )

        with col2:
            st.markdown("### AI-teamet")
            st.image("resources/image66.png", width=450)

        with col3:
            st.markdown("### Nora Gjøen-Gjøsæter")
            st.markdown("Data Scientist ... ")
            st.image(
                "http://t1.gstatic.com/licensed-image?q=tbn:ANd9GcSL6uEj3tSYgKCJXpHn-A9UuJiKFRPR5c9ZbrHBtbQWdlXey-_bNBpE8s97lgDEpjc2",
                width=300,
            )
            st.markdown("nora@kantega.no")
