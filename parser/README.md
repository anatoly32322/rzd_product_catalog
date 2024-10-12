# Yandex Market parser
Для обучения модели мы взяли данные из Yandex Market. У Яндекса есть публичное API, позволяющее получить данные об аттрибутах конкретной категории.
## Usage
```
python3 yamarket.py [source_filepath]
```
`[source_filepath]` - путь до валидного json файла.
На выходе вы получите файл `output.json` - все данные, полученные из открытого API.