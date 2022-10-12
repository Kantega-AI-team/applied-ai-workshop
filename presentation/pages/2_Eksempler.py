import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
from utils.defaults import defaults
from utils.detr import detect, detr, plot_results, transform
from utils.kantega import kantega_footer

defaults()
st.markdown("# Eksempler")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Diskriminerende redning",
        "Optimalisert bilplassering",
        "Live objektdeteksjon",
        "Avansert objektdeteksjon",
        "Kjønnsidentifisering",
    ]
)

with tab1:
    col0, col1, col2, col3 = st.columns([1, 2, 2, 1])
    with col0:
        st.text(" ")

    with col1:
        st.markdown("### Treningsdata")
        df_train = pd.read_csv("resources/redning_input.csv", sep=";")
        st.dataframe(df_train)

    with col2:
        st.markdown("### Prediksjon")
        df_test = pd.read_csv("resources/redning_output.csv", sep=";")
        st.dataframe(df_test)

with tab2:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.empty()
    with col2:
        st.markdown("### Optimal plassering?")
        st.image("resources/dele2.png")
    with col3:
        st.image("resources/dele1.png")
    with col4:
        st.empty()


with tab3:
    col1, col2 = st.columns([1, 1])
    with col1:
        img_file_buffer = st.camera_input("Ta et bilde av noe")

    with col2:

        if img_file_buffer is not None:
            # To read image file buffer as a PIL Image
            img = Image.open(img_file_buffer)

            scores, boxes = detect(img, detr, transform)
            plot_results(img, scores, boxes)
        else:
            st.markdown("...")

with tab4:
    st.image(
        "https://media-exp1.licdn.com/dms/image/C4E22AQGK7KErb7oToA/feedshare-shrink_2048_1536/0/1659537910391?e=1665014400&v=beta&t=aOqqkprLrEW8maoPJ61nb-Uj3fiR2zMJ-Df0GxWBW-s",
        width=1200,
    )


with tab5:
    select = st.selectbox(label="Søk", options=["", "scientist", "stupid"])
    if select == "scientist":
        st.image("resources/image69.png")
    elif select == "stupid":
        st.image("resources/image70.jpeg")
    else:
        img = st.image("resources/image68.jpeg")

kantega_footer()
