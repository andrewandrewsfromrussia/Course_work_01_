import json
from datetime import datetime
from collections import defaultdict


def cashback_analyze(data: list, year: int, month: int) -> str:
    """
    Функция для анализа выгодности категорий повышенного кешбэка.
    :return: JSON строка.
    """

    cashback_dict = defaultdict(float)

    for transaction in data:
        transaction_date = transaction.get("Дата операции", "")
        try:
            transaction_datetime = datetime.strptime(transaction_date, "%d.%m.%Y %H:%M:%S")

            if transaction_datetime.year == year and transaction_datetime.month == month:
                category = transaction.get("Категория", "")
                spend = transaction.get("Сумма операции", 0)

                if category:
                    cashback_dict[category] += round(abs(spend) / 100, 2)
        except ValueError:
            continue

    sorted_cashback = dict(sorted(cashback_dict.items(), key=lambda item: item[1], reverse=True))

    sorted_cashback = {category: round(value, 2) for category, value in sorted_cashback.items()}

    return json.dumps(sorted_cashback, ensure_ascii=False, indent=4)