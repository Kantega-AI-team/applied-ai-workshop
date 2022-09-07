import graphviz
import streamlit as st
from utils.defaults import defaults

defaults()
st.markdown("# Oversikt")

tab0, tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Data science",
        "Kunstig intelligens",
        "Maskinlæring",
        "Veiledet læring",
        "Low code",
    ]
)
with tab0:
    show = False
    hva_gjor = st.text_input("")

    if all([word in hva_gjor.lower() for word in ["statistikk", "jobb"]]):
        st.image("resources/image22.jpeg", width=1500)

    elif all(
        [word in hva_gjor.lower() for word in ["hva", "gjør", "data", "scientist"]]
    ):
        st.image("resources/image25.png", width=1500)

    elif all(
        [word in hva_gjor.lower() for word in ["bør", "data", "scientist", "kunne"]]
    ):
        st.image("resources/image23.png", width=1500)


with tab1:
    graph = graphviz.Digraph(node_attr={"size": "20", "fontsize": "8", "shape": "egg"})
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
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        st.write(" ")
    with col2:
        st.image("resources/auto.png", width=600)
    with col3:
        for i in range(5):
            st.text("")

        st.markdown(
            """
            <div style="text-align: left ">         
            <i><h3>"A computer program is said to learn 
            from experience E with respect to some class of tasks T and performance measure P
            if its performance at tasks in T, 
            as measured by P, 
            improves with experience E"</i></h3></div>

                """,
            unsafe_allow_html=True,
        )
    with col4:
        st.empty()

with tab3:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.empty()
    with col2:
        selection = st.radio("", ["Student", "Maskinlæringsmodell"])
        if selection == "Student":
            st.image("resources/veiledet_laring.png")
        else:
            st.image("resources/sl.png")
    with col3:
        st.empty()

with tab4:
    col1, col2 = st.columns(2)
    with col1:
        st.image("resources/image57.png")
