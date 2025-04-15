import json
from typing import Any, Callable


def function_to_json(func: Callable[..., Any], *args: Any, **kwargs: Any) -> str:
    """
    Вызывает переданную функцию с аргументами и возвращает результат в JSON-формате.
    """
    result = func(*args, **kwargs)
    try:
        json_result = json.dumps(result, ensure_ascii=False, indent=4)
    except (TypeError, ValueError) as e:
        raise ValueError(f"Ошибка сериализации: {e}")
    return json_result
