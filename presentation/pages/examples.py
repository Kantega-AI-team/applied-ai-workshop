import numpy as np
import streamlit as st
from PIL import Image
from utils.detr import detect, detr, plot_results, transform

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
    img_file_buffer = st.camera_input("Ta et bilde av noe")

    if img_file_buffer is not None:
        # To read image file buffer as a PIL Image
        img = Image.open(img_file_buffer)

        scores, boxes = detect(img, detr, transform)
        plot_results(img, scores, boxes)

with tab4:
    st.header("AI snoozefunksjon ...eller?")
    img = st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
