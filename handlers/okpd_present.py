import numpy
import streamlit as st
import pandas as pd


@st.cache_resource
def csv_reader():
    with open("data/okpd2_best_matches.csv", "r") as csv_in:
        df = pd.read_csv(csv_in).set_index("OKPD2")
    return df


def handle():
    df = csv_reader()
    okpd = st.text_input("ОКПД")
    if okpd in df.index:
        st.write(df.loc[[okpd]])
