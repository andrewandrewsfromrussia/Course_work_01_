import pytest
import pandas as pd
from datetime import datetime
from src.reports import spending_by_category

@pytest.fixture
def sample_transactions():
    return pd.DataFrame([
        {"Дата операции": "10.02.2025", "Сумма операции": 1200, "Категория": "еда"},
        {"Дата операции": "15.03.2025", "Сумма операции": 800, "Категория": "еда"},
        {"Дата операции": "05.01.2025", "Сумма операции": 400, "Категория": "транспорт"},
        {"Дата операции": "10.11.2024", "Сумма операции": 300, "Категория": "еда"},
    ])

# Тест 1: Проверка фильтрации по категории и дате
def test_spending_by_category_with_date(sample_transactions):
    result = spending_by_category(sample_transactions, category="еда", date="15.03.2025")
    assert len(result) == 2, "Ожидается 2 записи по категории 'еда' за последние 3 месяца"
    assert all(result["Категория"] == "еда"), "Все записи должны быть категории 'еда'"
    assert all(pd.to_datetime(result["Дата операции"], dayfirst=True) <= pd.to_datetime("15.03.2025", dayfirst=True)), "Даты не должны быть позже 15.03.2025"

# Тест 2: Проверка фильтрации по категории и использования текущей даты
def test_spending_by_category_without_date(sample_transactions):
    current_date = datetime.now().strftime("%d.%m.%Y")  # получаем текущую дату как строку
    result = spending_by_category(sample_transactions, category="еда")
    assert len(result) == 2, f"Ожидается 2 записи по категории 'еда' за последние 3 месяца, текущая дата: {current_date}"

# Тест 3: Проверка с пустым датафреймом
def test_spending_with_empty_dataframe():
    empty_df = pd.DataFrame(columns=["Дата операции", "Сумма операции", "Категория"])
    result = spending_by_category(empty_df, category="еда", date="15.03.2025")
    assert result.empty, "Результат должен быть пустым для пустого датафрейма"

# Тест 4: Проверка на неверный формат даты
def test_spending_with_invalid_date_format(sample_transactions):
    with pytest.raises(ValueError):
        spending_by_category(sample_transactions, category="еда", date="invalid_date")

# Тест 5: Проверка, если категории нет в данных
def test_spending_with_category_not_found(sample_transactions):
    result = spending_by_category(sample_transactions, category="спорт", date="15.03.2025")
    assert result.empty, "Если категории нет, результат должен быть пустым"
