import streamlit as st


def kantega_footer():
    st.markdown("""---""")
    with st.expander("Hvem er det som snakker?"):

        col1, col2, col3 = st.columns(3)

        with col1:
            st.image("resources/kantega_logo.png", width=200)
            st.markdown(
                """
            #### Vi som jobber i Kantega mener vi har verdens beste arbeidsplass. 
            Vi eier alle like mye og vi jobber alle mot et felles mål. 
            
            I tillegg får vi jobbe med fantastiske kunder og viktige prosjekter som betyr mye for mange.
            
            Sjekk ut hva vi driver med kantega.no, eller send meg en mail på nora@kantega.no om du
            er interessert i å høre mer om oss."""
            )

        with col2:
            st.markdown("### Nora Gjøen-Gjøsæter")
            st.markdown("Data Scientist ... ")

        with col3:
            st.image(
                "http://t1.gstatic.com/licensed-image?q=tbn:ANd9GcSL6uEj3tSYgKCJXpHn-A9UuJiKFRPR5c9ZbrHBtbQWdlXey-_bNBpE8s97lgDEpjc2",
                width=300,
            )
