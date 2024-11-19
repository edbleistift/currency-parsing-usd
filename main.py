import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os

def get_usd_exchange_rate():
    today = datetime.now().strftime("%d.%m.%Y")
    print(f"Сегодняшняя дата: {today}")
    url = f"https://www.nationalbank.kz/ru/exchangerates/ezhednevnye-oficialnye-rynochnye-kursy-valyut/report?beginDate={today}&endDate={today}&rates%5B%5D=5"

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='table table-bordered table-striped text-size-xs')
        if not table:
            print("Таблица с курсами валют не найдена.")
            return None
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if len(columns) > 2:
                date_column = columns[0].text.strip()
                if date_column == datetime.now().strftime("%Y-%m-%d"):
                    usd_rate = columns[2].text.strip()
                    usd_rate = float(usd_rate.replace(',', '.'))
                    return usd_rate

        print("Данные о курсе доллара отсутствуют.")
        return None

    except requests.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None

def save_usd_rate_to_csv(rate):
    today = datetime.now().strftime("%Y-%m-%d")

    file_exists = os.path.isfile("C:\\Users\\eschiller\\Desktop\\currency_exchange_rate\\usd_exchange_rate.csv")

    with open("usd_exchange_rate.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Дата", "Курс доллара (KZT)"])

        writer.writerow([today, rate])

usd_rate = get_usd_exchange_rate()
if usd_rate is not None:
    print(f"Курс доллара на сегодня: {usd_rate} KZT")
    save_usd_rate_to_csv(usd_rate)
else:
    print("Не удалось получить курс доллара.")
