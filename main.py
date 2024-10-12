import streamlit as st
import handlers

st.set_page_config(page_title="markmap", layout="wide")

category_tree, okpd_to_rzd, specifications = st.tabs(["Дерево категорий", "ОКПД -> РЖД", "Выделение характеристик"])

with category_tree:
    handlers.tree_present.handle()

with okpd_to_rzd:
    handlers.okpd_present.handle()

with specifications:
    handlers.specifications_present.handle()
