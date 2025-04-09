import json
from utils import unated

def unated_json(data: list, date: str) -> str:
    """
    Преобразует ответ unated в JSON формат
    """
    result = unated(data, date)
    return json.dumps(result, ensure_ascii=False, indent=4)