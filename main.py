import streamlit as st

type_of_transaction = st.selectbox("Выберете вид сделки", ["Закупка товаров, работ, услуг", "Продажа/аренда недвижимости", "Продажа"])
st.write(f"Selected Option: {type_of_transaction!r}")

keywords = st.text_input("Ключевые слова")
st.write(keywords)
