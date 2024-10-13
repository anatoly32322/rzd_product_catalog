# giga_chat_functions.py

import requests
import json


# Функция для получения токена доступа
def get_access_token(credentials):
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    
    payload = {
        'scope': 'GIGACHAT_API_PERS'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': '24f98fbe-1b03-46ed-97bf-d52ae27ad01f',
        'Authorization': f'Basic {credentials}'  # Замените credentials на ваши данные
    }
    
    response = requests.post(url, headers=headers, data=payload, verify=False)
    return response.json()['access_token']


# Функция для запроса GigaChat с определёнными атрибутами
def gigachat_generate_category(access_token, title: str, description: str, client_id: str):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    
    message = f"""На основе информации о товаре с названием '{title}' и описанием '{description}', 
    выдели до 10 атрибутов и их значения в формате JSON: 
    {{"параметры": {{"параметр1": "значение1", "параметр2": "значение2"}}}}.
    Примеры атрибутов: количество (шт.), цвет, материал, вес, размер, объем, мощность, длина, ширина, высота и так далее. 
    Выдели какие могут быть параметры у данного товара, а также их значения."""

    payload = json.dumps({
        "model": "GigaChat",
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ],
        "stream": False,
        "repetition_penalty": 1
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Client-ID': client_id,
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.post(url, headers=headers, data=payload, verify=False)
    return json.loads(response.json()['choices'][0]['message']['content'])


if __name__ == "__main__":
    # Задайте свои данные
    CREDENTIALS = 'ваши_данные_для_доступа'  # Замените на ваши данные
    CLIENT_ID = 'ваш_client_id'  # Замените на ваш client ID

    # Получаем токен доступа
    ACCESS_TOKEN = get_access_token(CREDENTIALS)

    # Пример использования функции для генерации атрибутов
    title = "Пример товара"
    description = "Описание товара"
    
    # Запрос атрибутов
    attributes = gigachat_generate_category(ACCESS_TOKEN, title, description, CLIENT_ID)
    
    print("Сгенерированные атрибуты:", attributes)
