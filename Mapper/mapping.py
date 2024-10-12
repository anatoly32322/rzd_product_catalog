# mapping.py

import sqlite3
import pandas as pd
import json
from sentence_transformers import SentenceTransformer, util
import torch

def map_okpd2_to_category():
    """
    Функция для сопоставления кодов OKPD2 с новыми категориями 
    на основе векторных представлений.

    Returns:
        dict: Словарь, где ключ - код OKPD2, значение - новая категория 
              (полный путь до категории).
    """
    # Подключение к SQLite базе данных
    conn = sqlite3.connect('/repo/converted_database.db')
    
    # Загрузка данных из таблицы OKPD_2
    query = "SELECT OKPD2, OKPD2_NAME FROM OKPD_2"
    okpd2_data = pd.read_sql_query(query, conn)
    conn.close()

    # Загрузка дерева категорий из JSON файла
    with open('/repo/category_tree.json', 'r') as f:
        ozon_data = json.load(f)

    # Извлечение категорий
    def extract_categories(data, parent_names=None):
        records = []
        if parent_names is None:
            parent_names = []
        
        if 'children' in data:
            for child in data['children']:
                new_parent_names = parent_names + [data['name']]
                records.extend(extract_categories(child, new_parent_names))
        else:
            category_record = {'type_name': data['name'], 'type_id': data['id']}
            for i, parent_name in enumerate(parent_names):
                category_record[f'level_{i+1}_category'] = parent_name
            records.append(category_record)
        
        return records

    ozon_records = extract_categories(ozon_data['result'])
    ozon_df = pd.DataFrame(ozon_records)

    # Загрузка предобученной модели
    model = SentenceTransformer('deepvk/USER-bge-m3').to('cuda')

    # Преобразование названий в векторы
    okpd2_names = okpd2_data['OKPD2_NAME'].tolist()
    ozon_names = ozon_df['type_name'].tolist()

    okpd2_embeddings = model.encode(okpd2_names, convert_to_tensor=True, device='cuda')
    ozon_embeddings = model.encode(ozon_names, convert_to_tensor=True, device='cuda')

    # Вычисление косинусного сходства
    cosine_scores = util.pytorch_cos_sim(okpd2_embeddings, ozon_embeddings)

    # Нахождение лучших совпадений
    best_matches_cosine = []
    for i in range(len(okpd2_names)):
        best_index = cosine_scores[i].argmax()
        best_matches_cosine.append(ozon_names[best_index])

    # Создание словаря сопоставлений
    mapping_dict = dict(zip(okpd2_data['OKPD2'], best_matches_cosine))
    
    return mapping_dict

# Вызов функции для получения сопоставления
if __name__ == "__main__":
    mapping = map_okpd2_to_category()
    print(mapping)
