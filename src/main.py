"""Главный файл(файл для запуска)"""
import collections
import json
import os
import csv
import time
import requests

from bs4 import BeautifulSoup

from logger import logger
from color_text import out_red, out_yellow, out_blue


proxies = []
headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/86.0.4240.183 Mobile Safari/537.36"
}

# создаем именованный кортеж
ParseResult = collections.namedtuple(
    'ParseResult',
    (
        'address',
        'port',
        'type_',
    ),
)

# имена столбцов таблицы
HEADERS = (
    'Адрес',
    'Порт',
    'Тип',
)


def search_proxies(url):
    """Сохраняет список из прокси адресов в файл json"""
    number = int(input("Введите колличество прокси адресов: "))
    if number > 100:
        out_red("Куда тебе столько?)")
        time.sleep(2)
        os.system("clear")
        os.system("python main.py")
    else:
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.text, "lxml")
        for item in soup.find_all("tr")[:number]:
            try:
                # парсим страницу, выбирая параметры
                data = item.find_all("td")
                address = data[0].text
                port = data[1].text
                type_ = data[4].text
                proxies.append({
                    "Адрес": address,
                    "Порт": port,
                    "Тип": type_,
                })

                # заполняем таблицу данными
                proxies.append(ParseResult(
                    address=address,
                    port=port,
                    type_=type_,
                ))
            except IndexError:
                pass

        if os.path.exists("data_dir"):
            out_yellow(f"Обновляем данные о прокси")
            time.sleep(2)
            os.remove("data_dir/projects_data.json")
            out_blue("Данные успешно обновлены")
        else:
            os.mkdir("data_dir/")

        with open("data_dir/projects_data.json", "a", encoding="utf-8") as file:
            json.dump(proxies, file, indent=4, ensure_ascii=False)

        save_csv()


def save_csv():
    """Сохраняет данные в csv таблицу"""
    if not os.path.exists("result_csv"):
        os.mkdir("result_csv")
    path_file = 'result_csv/main.csv'
    with open(path_file, 'w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(HEADERS)
        for item in proxies:
            writer.writerow(item)


@logger.catch
def main():
    """Запускает скрипт"""
    search_proxies(url="https://www.sslproxies.org/")


if __name__ == '__main__':
    main()
