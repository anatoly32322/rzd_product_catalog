# Преобразование каталога товаров ОАО «РЖД»

## Yandex Cloud
Yandex Cloud используется для запросов к API YaGPT. Для корректной работы API, необходимо перед запуском указать `IAM_TOKEN` и `FOLDER_ID`. 
Подробное описание, как можно получить значения токена и folder_id, можно найти [тут](https://yandex.cloud/ru/docs/foundation-models/quickstart/yandexgpt)
```bash
export FOLDER_ID=<идентификатор_каталога>
export IAM_TOKEN=<IAM-токен>
curl \
  --request POST \
  --header "Content-Type: application/json" \
  --header "Authorization: Bearer ${IAM_TOKEN}" \
  --header "x-folder-id: ${FOLDER_ID}" \
  --data "@prompt.json" \
  "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
```

## Usage
Весь проект запускается в Docker-контейнере.

Сначала экспортируем нужные переменные окружения:
```bash
export FOLDER_ID=<идентификатор_каталога>
export IAM_TOKEN=<IAM-токен>
```

Соберем образ:
```bash
docker build --tag 'app' --build-arg iam_token=$IAM_TOKEN --build-arg folder_id=$FOLDER_ID .
```

Запускаем образ с прокидыванием портов:
```bash
docker run -p 8501:8501 'app'
```