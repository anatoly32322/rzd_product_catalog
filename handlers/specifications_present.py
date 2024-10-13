#
import os

import streamlit as st
import json
import requests


url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"


@st.cache_data
def get_base_prompt():
    """
    Получаем базовые промпт в формате, нужном YaGPT.
    :return: Промпт в json формате
    """
    with open("yc/prompt.json", "r") as fin:
        prompt = json.loads(fin.read())
    return prompt


def do_request(text: str):
    """
    Выполняет запрос к API YaGPT.
    :param text: Текст запроса
    :return: API response
    """
    prompt = get_base_prompt()
    prompt["modelUri"] = prompt["modelUri"].format(os.getenv("FOLDER_ID"))
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('IAM_TOKEN')}",
        "x-folder-id": os.getenv("FOLDER_ID")
    }
    prompt["messages"].append({
      "role": "user",
      "text": text
    })
    return requests.post(url, json=prompt, headers=headers)


def exec_request(text: str) -> dict:
    """
    Выполняет запрос и приводит ответ API к нужному нам виду.
    :param text: Текст, который передал пользователь
    :return: Результат обработки запроса в формате json
    """
    response = do_request(text)
    try:
        # Формат вывода заранее известен
        text_result = response.json()["result"]["alternatives"][0]["message"]["text"].strip("`")
        result = json.loads(text_result)
    except Exception:
        return {}
    return result


def handle():
    """
    Обработка запроса на разбиение введенного товара на аттрибуты.
    """
    string = st.text_input("Введите описание товара")
    result_json = exec_request(string)
    st.json(result_json)
