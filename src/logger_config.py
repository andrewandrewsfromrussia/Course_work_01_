import logging
import os
from logging import Logger

LOG_DIR = "../logs"
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"


def setup_logger(
    function_name: str, log_dir: str = LOG_DIR, level: int = LOG_LEVEL, log_format: str = LOG_FORMAT
) -> Logger:
    """
    Настройки логгера.
    :param function_name: имя функции.
    :param log_dir: папка с логами.
    :param level: уровень логирования по умолчанию.
    :param log_format: формат сообщения.
    """

    log_file = os.path.join(log_dir, f"{function_name}.log")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger = logging.getLogger(function_name)
    logger.setLevel(level)

    fh = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    fh.setLevel(level)

    formatter = logging.Formatter(log_format)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    return logger
