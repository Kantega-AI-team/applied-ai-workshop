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

            """
            )
            st.video("https://www.youtube.com/watch?v=B4PWHtlukMU")

        with col2:
            st.markdown("### AI-teamet")
            st.image("resources/image66.png", width=450)
            st.markdown(
                """ 
            En fantastisk gjeng som har samlet seg om et felles mål:

            #### Å levere ansvarlige og bærekraftige maskinlæringsløsninger som skaper verdi
            """
            )

        with col3:
            button = st.button("x")
            if button:
                st.markdown("### Viktor Hansen")
                st.markdown("Full stack data engineer og medeier")
                st.image(
                    "https://intranettfiles.blob.core.windows.net/ansatt-bilder/vikhan.jpeg?sv=2021-08-06&spr=https&st=2022-09-09T01%3A16%3A22Z&se=2022-09-16T01%3A16%3A22Z&sr=c&sp=r&sig=iX93b%2FVWdfLNqrsrgZDazIxsB4%2FeVbuHP5%2Fqgc2iRF0%3D"
                )
            else:
                st.markdown("### Nora Gjøen-Gjøsæter")
                st.markdown("Data Scientist og medeier")
                st.image(
                    "http://t1.gstatic.com/licensed-image?q=tbn:ANd9GcSL6uEj3tSYgKCJXpHn-A9UuJiKFRPR5c9ZbrHBtbQWdlXey-_bNBpE8s97lgDEpjc2",
                    width=300,
                )
                st.markdown("...og tidligere fotballspiller")

        st.empty()
        st.empty()
        st.markdown(
            "##### *Vi eier alle like mye og vi jobber alle mot et felles mål. I tillegg får vi jobbe med fantastiske kunder og viktige prosjekter som betyr mye for mange.* "
        )
