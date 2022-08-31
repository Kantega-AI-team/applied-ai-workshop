import numpy as np
import streamlit as st
from PIL import Image
from utils.defaults import defaults
from utils.detr import detect, detr, plot_results, transform
from utils.kantega import kantega_footer

defaults()
st.markdown("# Eksempler")

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Diskriminerende redning",
        "Optimalisert bilplassering",
        "Objektdeteksjon på echo",
        "Kjønnsidentifisering",
    ]
)

with tab1:
    col1, col2 = st.columns(2, gap="small")
    with col1:
        st.markdown("### Treningsdata")
        st.markdown(
            """

        | kunde | antall produkter | alder | postnummer | ble reddet |
        |-------|------------------|-------|--------|------------|
        | Ola   | 3                | 34    | 5028   | ja         |
        | Kari  | 5                | 21    | 5071   | ja         |
        | Trond | 6                | 49    | 0612   | nei        |
        | Siv   | 1                | 22    | 3429   | nei        |
        | Lars  | 1                | 23    | 5253   | ja         |
        | Frode | 1                | 62    | 5254   | nei        |
        | Ove   | 1                | 37    | 4078   | ja         |
        | Jonas | 3                | 62    | 5012   | nei        |
        | Atle  | 3                | 73    | 5071   | nei        |
        | Liv   | 2                | 50    | 5071   | nei        |
        """
        )

    with col2:
        st.markdown("### Prediksjon")
        st.markdown(
            """

            | kunde | antall produkter | alder | postnummer | blir reddet |
        |-------|------------------|-------|--------|------------|
        | Per   | 4               | 63    | 0820   | 56%         |
        | Pål  | 1                | 19    | 5038   | 57%         |
        | Espen   | 1                | 39    | 5245   | 83%        |
        | Grete   | 1                | 32    | 5245   | 21%        |
        
            """
        )

with tab2:
    st.header("Optimalisert bilplassering")

with tab3:
    st.header("Objektdeteksjon på echo")
    img_file_buffer = st.camera_input("Ta et bilde av noe")

    if img_file_buffer is not None:
        # To read image file buffer as a PIL Image
        img = Image.open(img_file_buffer)

        scores, boxes = detect(img, detr, transform)
        plot_results(img, scores, boxes)

with tab4:
    st.header("Kjønnsidentifisering")
    img = st.image("resources/image68.jpeg")


kantega_footer()
