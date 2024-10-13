import streamlit as st
from streamlit_markmap import markmap


@st.cache_data
def load_data() -> str:
    """
    Загружает данные для отображения в формате markdown.
    Подробнее про формат можно прочитать в json_to_md_converter/README.md
    :return: Данные в формате markdown
    """
    with open("data/category_tree.md", "r") as fin:
        content = fin.read()
    return content


def handle():
    """
    Обработка запроса на получение дерева категорий.
    """
    content = load_data()
    markmap(content, height=1000)
