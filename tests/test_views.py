import json
from unittest.mock import patch

from src.views import unated_json

@patch("src.views.unated")
def test_unated_json_success(mock_unated):
    mock_unated.return_value = {
        "greeting": "Доброе утро",
        "cards": [{"cashback": 5.0, "last_digits": "1234", "total_spend": 1500}],
        "top_transactions": [{"amount": 1000}],
        "currency_rates": {"EUR": 96.5, "USD": 89.7},
        "stock_prices": {"SPY": 400.1, "GOOGL": 2900.2}
    }

    data = [{"dummy": "data"}]
    date = "2025-04-10 07:00:00"

    result = unated_json(data, date)
    parsed = json.loads(result)

    assert isinstance(parsed, dict)
    assert parsed["greeting"] == "Доброе утро"
    assert parsed["cards"][0]["last_digits"] == "1234"
    assert parsed["top_transactions"][0]["amount"] == 1000
    assert parsed["currency_rates"]["USD"] == 89.7