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

    elif all(
        [word in hva_gjor.lower() for word in ["bør", "data", "scientist", "kunne"]]
    ):
        st.image("resources/image23.png", width=1500)


with tab1:
    graph = graphviz.Digraph(node_attr={"size": "20", "fontsize": "10"})
    graph.edge("Kunstig intelligens", "Maskinlæring")
    graph.edge("Kunstig intelligens", "GOFAI")
    graph.node("Maskinlæring", _attributes={"color": "#F49727"})
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
    graph.edge("Regresjon", "Nevrale nettverk")
    graph.edge("Klassifisering", "Random Forest ")
    graph.edge("Klassifisering", "Nevrale nettverk ")
    st.graphviz_chart(graph, use_container_width=True)


with tab2:
    st.markdown("""
         ### "A computer program is said to learn 
         #### from experience **E** with respect to some class of tasks **T** and performance measure **P** 
         #### if its performance at tasks in T, 
         #### as measured by P, 
         ### improves with experience E"
    """
    )

with tab3:
    st.image("resources/veiledet_laring.png")