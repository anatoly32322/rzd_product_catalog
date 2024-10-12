import streamlit as st
from streamlit_markmap import markmap


@st.cache_data
def load_data() -> str:
    with open("data/category_tree.md", "r") as fin:
        content = fin.read()
    return content


def handle():
    content = load_data()
    markmap(content, height=1000)
