import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os

def get_usd_exchange_rate():
    # Определяем текущую дату
    today = datetime.now().strftime("%d.%m.%Y")  # Формат даты DD.MM.YYYY
    print(f"Сегодняшняя дата: {today}")

    # Формируем URL с текущей датой
    url = f"https://www.nationalbank.kz/ru/exchangerates/ezhednevnye-oficialnye-rynochnye-kursy-valyut/report?beginDate={today}&endDate={today}&rates%5B%5D=5"

    try:
        # Отправляем запрос на сайт
        response = requests.get(url)
        response.raise_for_status()  # Проверяем успешность запроса

        # Парсим HTML-страницу
        soup = BeautifulSoup(response.text, 'html.parser')

        # Ищем таблицу с курсами
        table = soup.find('table', class_='table table-bordered table-striped text-size-xs')
        if not table:
            print("Таблица с курсами валют не найдена.")
            return None

        # Ищем строки таблицы
        rows = table.find_all('tr')  # Все строки таблицы
        for row in rows:
            columns = row.find_all('td')  # Столбцы в строке
            if len(columns) > 2:
                date_column = columns[0].text.strip()  # Проверяем дату
                if date_column == datetime.now().strftime("%Y-%m-%d"):  # Сравниваем с текущей датой
                    usd_rate = columns[2].text.strip()  # Курс доллара в третьем столбце
                    usd_rate = float(usd_rate.replace(',', '.'))  # Преобразуем в число
                    return usd_rate

        print("Данные о курсе доллара отсутствуют.")
        return None

    except requests.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None

def save_usd_rate_to_csv(rate):
    today = datetime.now().strftime("%Y-%m-%d")  # Формат даты для CSV

    # Проверяем, существует ли файл
    file_exists = os.path.isfile("usd_exchange_rate.csv")

    # Открываем файл в режиме добавления
    with open("usd_exchange_rate.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        # Если файл только создается, добавляем заголовок
        if not file_exists:
            writer.writerow(["Дата", "Курс доллара (KZT)"])

        # Записываем курс и дату
        writer.writerow([today, rate])

# Получаем курс доллара и сохраняем его в CSV
usd_rate = get_usd_exchange_rate()
if usd_rate is not None:
    print(f"Курс доллара на сегодня: {usd_rate} KZT")
    save_usd_rate_to_csv(usd_rate)
else:
    print("Не удалось получить курс доллара.")