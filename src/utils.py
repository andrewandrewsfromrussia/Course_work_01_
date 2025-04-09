import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

from src.logger_config import setup_logger

load_dotenv()

file_path = os.getenv("DATA_FILE_PATH")
api_key = os.getenv("API_KEY")


def read_xlsx_file(file_path: str) -> list | None:
    """
    Функция для чтения XLSX файлов.
    :param file_path: Путь к XLSX файлу.
    :return: Список словарей.
    """
    logger = setup_logger(read_xlsx_file.__name__)

    try:
        logger.info(f"Запуск read_xlsx_file. Ищу файл {file_path}...")
        df = pd.read_excel(file_path)
        data = df.to_dict(orient="records")
        logger.info("Успешно.")
        return data
    except FileNotFoundError:
        logger.exception(f"Ошибка: файл {file_path} не найден.")
        return None
    except Exception as e:
        logger.exception(f"Ошибка при чтении файла {file_path}: {e}")
        return None


def greeting(date: str) -> str | None:
    """
    Функция отработки приветственного сообщения в зависимости от времени.
    :return: Строка приветствия.
    """
    logger = setup_logger(greeting.__name__)

    logger.info("Запуск greeting. Определение формата времени.")
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        date_hour = date_obj.hour

    except Exception as e:
        logger.exception(f"Ошибка: {e}")
        return None

    try:
        if 6 <= date_hour <= 12:
            return "Доброе утро"
        elif 12 <= date_hour <= 18:
            return "Добрый день"
        elif 18 <= date_hour <= 24:
            return "Добрый вечер"
        else:
            return "Доброй ночи"

    except Exception as e:
        logger.exception(f"Ошибка: {e}")
        return None


def cards(data: list) -> list:
    """
    Функция обработки xlsx файла.
    :return: Последние 4 цифры карты, общую сумма расходов, кешбэк.
    """
    logger = setup_logger(cards.__name__)

    logger.info("Инициализация списка.")
    cards_info: list[dict] = []
    logger.info("Успешно. Инициализация итерации поиска.")
    for key in data:
        card_number = str(key.get("Номер карты", "")).replace(" ", "")[-4:]
        spend = key.get("Сумма операции", 0)

        found = False
        for card in cards_info:
            if card_number == card["last_digits"]:
                card["total_spend"] += spend
                found = True
                break

        if not found:
            cards_info.append({"last_digits": card_number, "total_spend": spend, "cashback": 0})

    logger.info("Успешно. Инициализация форматирования значений.")
    for option in cards_info:
        option["cashback"] = round(abs(option["total_spend"] / 100), 2)
        option["total_spend"] = round(abs(option["total_spend"]), 2)

    logger.info("Успешно. Завершение программы.")

    return cards_info


def top_transactions(data: list) -> list:
    """
    Функция определения топ-5 транзакций по сумме платежа.
    :return: Список словарей.
    """
    logger = setup_logger(top_transactions.__name__)

    logger.info("Инициализация списка.")
    top_transaction = []

    logger.info("Успешно. Инициализация итерации поиска.")
    for key in data:
        transaction = {
            "date": key.get("Дата операции"),
            "amount": key.get("Сумма операции", 0),
            "category": key.get("Категория"),
            "description": key.get("Описание"),
        }

        top_transaction.append(transaction)

        top_transaction = sorted(top_transaction, key=lambda x: x["amount"], reverse=True)[:5]

    logger.info("Успешно. Завершение работы программы.")

    return top_transaction


def currency_rates(*currencies: str) -> list | None:
    """
    Функция для запроса курса валют у стороннего API.
    :return: Список словарей с курсом валют.
    """
    logger = setup_logger(currency_rates.__name__)

    logger.info("Инициализация работы функции.")
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    logger.info(f"url: | {url} | добавлен успешно.")

    logger.info("Инициализация подключения.")
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        logger.info("Инициализация списка.")
        c_rates = []

        logger.info("Успешно. Итерирование ответа API.")
        for currency in currencies:
            rate = data["Valute"].get(currency, {}).get("Value")
            if rate:
                logger.info("Курс найден.")
                c_rates.append({"currency": currency, "rate": round(rate, 2)})
            else:
                logger.info("Курс не найден.")
                c_rates.append({"currency": currency, "rate": "Курс не найден"})

        logger.info("Успешно. Завершение работы программы.")
        return c_rates

    except requests.RequestException as e:
        logger.exception(f"Ошибка: {e}")
        return None


def stock_prices(*symbols: str) -> list:
    """
    Получает текущие цены акций.
    :return: Список словарей с ценами акций.
    """
    logger = setup_logger(stock_prices.__name__)

    logger.info("Инициализация работы функции.")
    url = "https://www.alphavantage.co/query"
    logger.info(f"url: | {url} | добавлен успешно.")

    logger.info("Инициализация списка.")
    stock_price = []
    logger.info("Успешно")

    logger.info("Итерирование словарей.")
    for symbol in symbols:
        params = {"function": "GLOBAL_QUOTE", "symbol": symbol, "apikey": api_key}

        logger.info("Инициализация подключения.")
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            price = data.get("Global Quote", {}).get("05. price")
            if price:
                logger.info("Цена найдена")
                stock_price.append({"stock": symbol, "price": round(float(price), 2)})
            else:
                logger.info("Цена не найдена")
                stock_price.append({"stock": symbol, "price": "Цена не найдена"})

        except requests.RequestException as e:
            logger.exception(f"Ошибка: {e}")
            stock_price.append({"stock": symbol, "price": f"Ошибка запроса: {e}"})

    logger.info("Успешно. Завершение работы программы.")
    return stock_price


def unated(data: list, date: str) -> dict:
    """
    Функция объединяющая модуль.
    :param data: Файл с данными об операциях.
    :param date: Используемая дата.
    :return: Словарь со значениями.
    """
    logger = setup_logger(unated.__name__)

    logger.info("Инициализация работы функции.")
    unated_ = {
        "greeting": greeting(date),
        "cards": cards(data),
        "top_transactions": top_transactions(data),
        "currency_rates": currency_rates("EUR", "USD"),
        "stock_prices": stock_prices("SPY", "GOOGL"),
    }
    logger.info("Успешно. Завершение работы программы.")
    return unated_
