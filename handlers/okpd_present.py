import numpy
import streamlit as st
import pandas as pd


@st.cache_resource
def csv_reader():
    """
    Читает файл .csv и преобразует данные в нужный нам формат.
    Формат: преобразует набор колонок с уровнями категорий к виду
    level_1_category > level_2_category > ... > best_match.
    :return: DataFrame с индексом на OKPD2
    """
    with open("data/okpd2_best_matches.csv", "r") as csv_in:
        df = pd.read_csv(csv_in)
    categories_cols = [
        'level_1_category',
        'level_2_category',
        'level_3_category',
        'level_4_category',
        'level_5_category',
        'level_6_category',
        'best_match'
    ]
    df['NEW_CATEGORY'] = df[categories_cols].apply(lambda row: ' > '.join(row.dropna()), axis=1)
    final_df = df[['OKPD2', 'OKPD2_NAME', 'NEW_CATEGORY']]

    return final_df.set_index("OKPD2")


def handle():
    """
    Обработка запроса на получение информации по конкретному ОКПД.
    """
    df = csv_reader()
    okpd = st.text_input("ОКПД")
    if okpd in df.index:
        st.write(df.loc[[okpd]])
    else:
        st.write(df)
