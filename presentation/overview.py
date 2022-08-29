import streamlit as st


def overview():
    st.markdown("# Oversikt")
    st.sidebar.markdown("# Oversikt")

    st.expander(
        "ml_def",
        expanded=st.markdown(
            "### A computer program is said to learn from experience E with respect to some class of tasks T and performance measure P if its performance at tasks in T, as measured by P, improves with experience E"
        ),
    )
