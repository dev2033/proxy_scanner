"""Главный файл(файл для запуска)"""
import json
import os
import time
import requests

from bs4 import BeautifulSoup

from logger import logger


proxies = []
headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/86.0.4240.183 Mobile Safari/537.36"
}


def search_proxies(url):
    """Выводит список из прокси адресов"""
    number = int(input("Введите колличество прокси адресов: "))
    num = 1
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.text, "lxml")
    for item in soup.find_all("tr")[:number]:
        try:
            data = item.find_all("td")
            address = data[0].text
            port = data[1].text
            type_ = data[4].text
            proxies.append({str(num) + " адрес": {
                "Адрес": address,
                "Порт": port,
                "Тип": type_,
            }})
            num += 1
        except IndexError:
            pass

    if os.path.exists("data_dir"):
        print(f"Обновляем данные о прокси")
        time.sleep(2)
        os.remove("data_dir/projects_data.json")
        print("Данные успешно обновлены")
    else:
        os.mkdir("data_dir/")

    with open("data_dir/projects_data.json", "a", encoding="utf-8") as file:
        json.dump(proxies, file, indent=4, ensure_ascii=False)


@logger.catch
def main():
    search_proxies(url="https://www.sslproxies.org/")


if __name__ == '__main__':
    main()
