import json
from datetime import datetime
from functools import wraps
from typing import Optional

import pandas as pd

from src.logger_config import setup_logger


def save_report(filename=None):
    """
    Декоратор для функций отчетов, записывает результат в файл. Можно записывать с параметром названия файла или без.
    """

    def actual_save(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            actual_filename = filename
            if actual_filename is None:
                actual_filename = f"report_{func.__name__}.json"

            try:
                if isinstance(result, pd.DataFrame):
                    result.to_json(
                        actual_filename, orient="records", force_ascii=False, indent=4
                    )
                else:
                    with open(actual_filename, "w", encoding="utf-8") as f:
                        json.dump(result, f, ensure_ascii=False, indent=4)

            except Exception as e:
                print(f"Ошибка: {e}")

            return result

        return wrapper

    if callable(filename):
        func = filename
        filename = None
        return actual_save(func)

    return actual_save


@save_report()
def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> pd.DataFrame:
    """
    Возвращает траты по категории за последние 3 месяца от переданной даты.
    Если дата не передана - используется текущая дата.
    """

    logger = setup_logger(spending_by_category.__name__)

    if date:
        logger.info("Обнаружена дата.")
        current_date = pd.to_datetime(date, dayfirst=True)
    else:
        logger.info("Дата не обнаружена.")
        current_date = pd.to_datetime(datetime.now())

    three_months_ago = current_date - pd.DateOffset(months=3)

    logger.info("Фильтрация данных.")
    filtered = transactions[
        (transactions["Категория"] == category)
        & (
            pd.to_datetime(transactions["Дата операции"], dayfirst=True)
            >= three_months_ago
        )
        & (pd.to_datetime(transactions["Дата операции"], dayfirst=True) <= current_date)
    ]

    logger.info("Завершение работы функции.")
    return filtered
