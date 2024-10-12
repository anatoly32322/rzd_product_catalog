import codecs
import json
import os
import sys
import time
import logging
import requests


logging.basicConfig(level=logging.INFO)
counter = 50  # Yandex Market API имеет ограничение на 50 запросов в минуту
headers = {"Authorization": f"Bearer {os.getenv('OAUTH_TOKEN')}"}
formatted_url = "https://api.partner.market.yandex.ru/category/{}/parameters"
fout = codecs.open("output.json", "w+", "utf-8")
results = []


def dfs(category: dict):
    global counter
    if counter == 0:
        logging.info("go to sleep")
        time.sleep(60)
        counter = 50
    if category.get("children") is None:
        content = requests.post(formatted_url.format(category["id"]), headers=headers)
        results.append(content.json())
        counter -= 1
        logging.info(f"processed leaf with status_code: {content.status_code}")
        return
    for child in category["children"]:
        dfs(child)


def run(args: list):
    filepath = args[1]
    if not os.path.exists(filepath):
        print("Wrong filepath")
        return
    with open(filepath, "r") as fin:
        dfs(json.loads(fin.read())["result"])
    fout.write(json.dumps(results, indent=4, ensure_ascii=False).encode('utf8').decode())


if __name__ == "__main__":
    run(sys.argv)
fout.close()
