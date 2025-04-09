from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from src.utils import cards, currency_rates, greeting, read_xlsx_file, stock_prices, top_transactions, unated


@pytest.mark.parametrize(
    "file_path, mock_return_value, expected",
    [
        (
            "valid_file.xlsx",
            [{"Card": "Visa", "Value": 300}],
            [{"Card": "Visa", "Value": 300}],
        ),
        ("empty_file.xlsx", [], []),
    ],
)
@patch("src.utils.pd.read_excel")
def test_read_xlsx_file_valid(
    mock_read_excel: MagicMock, file_path: str, mock_return_value: Any, expected: Any
) -> None:
    """
    Тест на успешное чтение файлов.
    """
    mock_df = MagicMock()
    mock_df.to_dict.return_value = mock_return_value
    mock_read_excel.return_value = mock_df

    assert read_xlsx_file(file_path) == expected


@patch("src.utils.setup_logger")
def test_greeting_morning(mock_setup_logger: MagicMock) -> None:
    mock_logger = MagicMock()
    mock_setup_logger.return_value = mock_logger

    result = greeting("2025-04-06 07:30:00")
    assert result == "Доброе утро"

    mock_logger.info.assert_any_call("Запуск greeting. Определение формата времени.")


@patch("src.utils.setup_logger")
def test_greeting_invalid_date(mock_setup_logger: MagicMock) -> None:
    mock_logger = MagicMock()
    mock_setup_logger.return_value = mock_logger

    result = greeting("Invalid_date")

    assert result is None

    mock_logger.exception.assert_called_with(
        "Ошибка: time data 'Invalid_date' does not match format '%Y-%m-%d %H:%M:%S'"
    )


@patch("src.utils.setup_logger")
def test_cards_entries(mock_setup_logger: MagicMock) -> None:
    """
    Тест на обработку данных, когда одна и та же карта встречается несколько раз.
    """
    mock_logger = MagicMock()
    mock_setup_logger.return_value = mock_logger

    data = [
        {"Номер карты": "1234 5678 9012 3456", "Сумма операции": 100},
        {"Номер карты": "1234 5678 9012 3456", "Сумма операции": 200},
        {"Номер карты": "1234 5678 9012 3457", "Сумма операции": 300},
    ]

    result = cards(data)

    expected = [
        {"last_digits": "3456", "total_spend": 300.00, "cashback": 3.00},
        {"last_digits": "3457", "total_spend": 300.00, "cashback": 3.00},
    ]

    assert result == expected
    mock_logger.info.assert_any_call("Успешно. Завершение программы.")


@patch("src.utils.setup_logger")
def test_cards_new_card(mock_setup_logger: MagicMock) -> None:
    """
    Тест на обработку новой карты.
    """
    mock_logger = MagicMock()
    mock_setup_logger.return_value = mock_logger

    data = [
        {"Номер карты": "1234 5678 9012 3456", "Сумма операции": 100},
        {"Номер карты": "1234 5678 9012 3457", "Сумма операции": 500},
    ]

    result = cards(data)

    expected = [
        {"last_digits": "3456", "total_spend": 100.00, "cashback": 1.00},
        {"last_digits": "3457", "total_spend": 500.00, "cashback": 5.00},
    ]

    assert result == expected
    mock_logger.info.assert_any_call("Успешно. Завершение программы.")


@patch("src.utils.setup_logger")
def test_top_transactions_less_than_5(mock_setup_logger: MagicMock) -> None:
    """
    Тест на случай, если транзакций меньше 5.
    """
    mock_logger = MagicMock()
    mock_setup_logger.return_value = mock_logger

    data = [
        {
            "Дата операции": "2025-04-01",
            "Сумма операции": 100,
            "Категория": "Продукты",
            "Описание": "Покупка в магазине",
        },
        {
            "Дата операции": "2025-04-02",
            "Сумма операции": 300,
            "Категория": "Электроника",
            "Описание": "Покупка ноутбука",
        },
        {
            "Дата операции": "2025-04-03",
            "Сумма операции": 200,
            "Категория": "Одежда",
            "Описание": "Покупка джинсов",
        },
    ]

    result = top_transactions(data)

    expected = [
        {
            "date": "2025-04-02",
            "amount": 300,
            "category": "Электроника",
            "description": "Покупка ноутбука",
        },
        {
            "date": "2025-04-03",
            "amount": 200,
            "category": "Одежда",
            "description": "Покупка джинсов",
        },
        {
            "date": "2025-04-01",
            "amount": 100,
            "category": "Продукты",
            "description": "Покупка в магазине",
        },
    ]

    assert result == expected
    mock_logger.info.assert_any_call("Успешно. Завершение работы программы.")


@patch("src.utils.setup_logger")
def test_top_transactions_5(mock_setup_logger: MagicMock) -> None:
    """
    Тест на случай, если транзакций меньше 5.
    """
    mock_logger = MagicMock()
    mock_setup_logger.return_value = mock_logger

    data = [
        {
            "Дата операции": "2025-04-01",
            "Сумма операции": 100,
            "Категория": "Продукты",
            "Описание": "Покупка в магазине",
        },
        {
            "Дата операции": "2025-04-02",
            "Сумма операции": 300,
            "Категория": "Электроника",
            "Описание": "Покупка ноутбука",
        },
        {
            "Дата операции": "2025-04-03",
            "Сумма операции": 200,
            "Категория": "Одежда",
            "Описание": "Покупка джинсов",
        },
    ]

    result = top_transactions(data)

    expected = [
        {
            "date": "2025-04-02",
            "amount": 300,
            "category": "Электроника",
            "description": "Покупка ноутбука",
        },
        {
            "date": "2025-04-03",
            "amount": 200,
            "category": "Одежда",
            "description": "Покупка джинсов",
        },
        {
            "date": "2025-04-01",
            "amount": 100,
            "category": "Продукты",
            "description": "Покупка в магазине",
        },
    ]

    assert result == expected
    mock_logger.info.assert_any_call("Успешно. Завершение работы программы.")


@patch("src.utils.setup_logger")
def test_top_transactions_empty(mock_setup_logger: MagicMock) -> None:
    """
    Тест на пустой список транзакций.
    """
    mock_logger = MagicMock()
    mock_setup_logger.return_value = mock_logger

    data: list = []

    result = top_transactions(data)

    expected: list = []

    assert result == expected
    mock_logger.info.assert_any_call("Успешно. Завершение работы программы.")


@patch("src.utils.setup_logger")
def test_top_transactions_zero_amount(mock_setup_logger: MagicMock) -> None:
    """
    Тест на транзакции с нулевыми суммами.
    """
    mock_logger = MagicMock()
    mock_setup_logger.return_value = mock_logger

    data = [
        {
            "Дата операции": "2025-04-01",
            "Сумма операции": 0,
            "Категория": "Продукты",
            "Описание": "Покупка в магазине",
        },
        {
            "Дата операции": "2025-04-02",
            "Сумма операции": 0,
            "Категория": "Электроника",
            "Описание": "Покупка ноутбука",
        },
        {
            "Дата операции": "2025-04-03",
            "Сумма операции": 0,
            "Категория": "Одежда",
            "Описание": "Покупка джинсов",
        },
    ]

    result = top_transactions(data)

    expected = [
        {
            "date": "2025-04-01",
            "amount": 0,
            "category": "Продукты",
            "description": "Покупка в магазине",
        },
        {
            "date": "2025-04-02",
            "amount": 0,
            "category": "Электроника",
            "description": "Покупка ноутбука",
        },
        {
            "date": "2025-04-03",
            "amount": 0,
            "category": "Одежда",
            "description": "Покупка джинсов",
        },
    ]

    assert result == expected
    mock_logger.info.assert_any_call("Успешно. Завершение работы программы.")


@patch("src.utils.requests.get")
def test_currency_rates_success(mock_get: MagicMock) -> None:
    """
    Тест на успешное соединение и получение курса доллара.
    """

    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {"Valute": {"USD": {"Value": 75.55}}}
    mock_get.return_value = mock_response

    result = currency_rates("USD")

    expected = [{"currency": "USD", "rate": 75.55}]

    assert result == expected, f"Expected {expected}, but got {result}"


@patch("src.utils.requests.get")
def test_currency_rates_no_data(mock_get: MagicMock) -> None:
    """
    Тест на случай, если курс валюты не найден в ответе.
    """

    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {"Valute": {}}
    mock_get.return_value = mock_response

    result = currency_rates("USD")

    expected = [{"currency": "USD", "rate": "Курс не найден"}]

    assert result == expected, f"Expected {expected}, but got {result}"


@patch("src.utils.requests.get")  # Патчим requests.get, чтобы заменить реальный запрос
def test_stock_prices_success(mock_get: MagicMock) -> None:
    """
    Тест на успешное соединение и получение цены акции.
    """

    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {"Global Quote": {"05. price": "150.25"}}
    mock_get.return_value = mock_response

    result = stock_prices("AAPL")

    expected = [{"stock": "AAPL", "price": 150.25}]

    assert result == expected, f"Expected {expected}, but got {result}"


@patch("src.utils.requests.get")
def test_stock_prices_no_data(mock_get: MagicMock) -> None:
    """
    Тест на случай, если цена акции не найдена в ответе.
    """

    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {"Global Quote": {}}
    mock_get.return_value = mock_response

    result = stock_prices("AAPL")

    expected = [{"stock": "AAPL", "price": "Цена не найдена"}]

    assert result == expected, f"Expected {expected}, but got {result}"


@patch("src.utils.greeting")
@patch("src.utils.cards")
@patch("src.utils.top_transactions")
@patch("src.utils.currency_rates")
@patch("src.utils.stock_prices")
def test_unated(
    mock_stock_prices: MagicMock,
    mock_currency_rates: MagicMock,
    mock_top_transactions: MagicMock,
    mock_cards: MagicMock,
    mock_greeting: MagicMock,
) -> None:
    """
    Тест для функции unated.
    """

    mock_greeting.return_value = "Hello"
    mock_cards.return_value = [
        {"last_digits": "3456", "total_spend": 100.0, "cashback": 1.0},
        {"last_digits": "3457", "total_spend": 500.0, "cashback": 5.0},
    ]
    mock_top_transactions.return_value = [
        {
            "date": "2025-04-01",
            "amount": 100.0,
            "category": "Продукты",
            "description": "Покупка в магазине",
        },
        {
            "date": "2025-04-02",
            "amount": 300.0,
            "category": "Электроника",
            "description": "Покупка ноутбука",
        },
    ]
    mock_currency_rates.return_value = [
        {"currency": "EUR", "rate": 88.0},
        {"currency": "USD", "rate": 75.0},
    ]
    mock_stock_prices.return_value = [
        {"stock": "SPY", "price": 400.0},
        {"stock": "GOOGL", "price": 2800.0},
    ]

    data = [{"Номер карты": "1234 5678 9012 3456", "Сумма операции": 100}]
    date = "2025-04-01"

    result = unated(data, date)

    expected = {
        "greeting": "Hello",
        "cards": [
            {"last_digits": "3456", "total_spend": 100.0, "cashback": 1.0},
            {"last_digits": "3457", "total_spend": 500.0, "cashback": 5.0},
        ],
        "top_transactions": [
            {
                "date": "2025-04-01",
                "amount": 100.0,
                "category": "Продукты",
                "description": "Покупка в магазине",
            },
            {
                "date": "2025-04-02",
                "amount": 300.0,
                "category": "Электроника",
                "description": "Покупка ноутбука",
            },
        ],
        "currency_rates": [
            {"currency": "EUR", "rate": 88.0},
            {"currency": "USD", "rate": 75.0},
        ],
        "stock_prices": [
            {"stock": "SPY", "price": 400.0},
            {"stock": "GOOGL", "price": 2800.0},
        ],
    }

    assert result == expected, f"Expected {expected}, but got {result}"
