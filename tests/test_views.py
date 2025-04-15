import json

import pytest

from src.views import function_to_json  # замените на свой путь


def sample_func(a: int, b: int) -> dict:
    return {"sum": a + b}


def non_serializable_func() -> set:
    return set([1, 2, 3])  # Множество не сериализуется в JSON по умолчанию


def test_function_to_json_success() -> None:
    result = function_to_json(sample_func, 2, 3)
    expected = json.dumps({"sum": 5}, ensure_ascii=False, indent=4)
    assert result == expected


def test_function_to_json_raises_on_non_serializable() -> None:
    with pytest.raises(ValueError) as exc_info:
        function_to_json(non_serializable_func)
    assert "Ошибка сериализации" in str(exc_info.value)
