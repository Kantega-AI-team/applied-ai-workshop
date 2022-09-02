import graphviz
import streamlit as st
from utils.defaults import defaults

defaults()
st.markdown("# Oversikt")

tab0, tab1, tab2, tab3 = st.tabs(
    ["Data science", "Kunstig intelligens", "Maskinlæring", "Veiledet læring"]
)
with tab0:
    show = False
    hva_gjor = st.text_input("")

    if all([word in hva_gjor.lower() for word in ["hva", "gjør", "data", "scientist"]]):
        st.image("resources/image25.png", width=1500)
    
    elif all([word in hva_gjor.lower() for word in ["bør", "data", "scientist", "kunne"]]):
        st.image("resources/image23.png", width=1500)


with tab1:
    graph = graphviz.Digraph(node_attr={"shape": "plaintext"})
    graph.edge("Kunstig intelligens", "Maskinlæring")
    graph.edge("Kunstig intelligens", "GOFAI")
    graph.edge("Maskinlæring", "Veiledet læring")
    graph.edge("Maskinlæring", "Ikke-veiledet læring")
    graph.edge("Ikke-veiledet læring", "Dimensjonsreduksjon")
    graph.edge("Dimensjonsreduksjon", "Prinsipalkomponentanalyse")
    graph.edge("Dimensjonsreduksjon", "Faktoranalyse")
    graph.edge("Ikke-veiledet læring", "Clustering")
    graph.edge("Clustering", "K means")
    graph.edge("Clustering", "DBSCAN")
    graph.edge("Ikke-veiledet læring", "Anomalideteksjon")
    graph.edge("Veiledet læring", "Regresjon")
    graph.edge("Veiledet læring", "Klassifisering")
    graph.edge("Regresjon", "Generaliserte lineære modeller")
    graph.edge("Regresjon", "Gradient Boosting")
    graph.edge("Regresjon", "Random Forest")
    graph.edge("Regresjon", "Nevrale nettverk")
    graph.edge("Klassifisering", "Random Forest ")
    graph.edge("Klassifisering", "Nevrale nettverk ")
    graph.edge("Klassifisering", "Beslutningstrær")

    st.graphviz_chart(graph)


with tab2:
    st.markdown("## Maskinlæring")
    st.markdown(
        "##### A computer program is said to learn from experience E with respect to some class of tasks T and performance measure P if its performance at tasks in T, as measured by P, improves with experience E"
    )

with tab3:
    st.markdown("## Veiledet læring")
    st.image("resources/veiledet_laring.png")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("resources/image47.png")
    with col2:
        st.image("resources/image49.png")
    with col3:
        st.image("resources/image48.png")
