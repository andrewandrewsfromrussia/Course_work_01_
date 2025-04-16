import os

import pandas as pd
from dotenv import load_dotenv

from reports import spending_by_category
from services import cashback_analyze
from utils import greeting, read_xlsx_file
from views import function_to_json

# Создать .env или подставить как параметр где необходимо:
# DATA_FILE_PATH = "../data/operations.xlsx"

load_dotenv()

file_path = os.getenv("DATA_FILE_PATH")

if __name__ == "__main__":
    work_flag = True
    user = input("Доброго времени суток! Как я могу к Вам обращаться?\n")
    print(f"Рад знакомству, {user}!")
    print("Список реализованных функций проекта на данный момент:")
    print("[1] read_xlsx_file - Функция для чтения XLSX файлов.")
    print("[2] greeting - Функция отработки приветственного сообщения в зависимости от времени.")
    print("[3] spending_by_category - Возвращает траты по категории за последние 3 месяца от переданной даты.")
    print("[4] cashback_analyze - Функция для анализа выгодности категорий повышенного кешбэка.")
    print("[5] function_to_json - Вызывает переданную функцию с аргументами и возвращает результат в JSON-формате.")

    while work_flag:
        command = input(f"{user}, введите команду: ")

        if command == "1":
            print("Вызываю функцию read_xlsx_file")
            try:

                result = read_xlsx_file(file_path=file_path)

                print("Функция запущена успешно!")
                if input("Хотите посмотреть результат? [yes/no]\n") == "yes":
                    print(result)
            except Exception as e:
                print(f"Произошла непредвиденная ошибка! {e}")

        elif command == "2":
            print("Вызываю функцию greeting")
            try:

                result = greeting(date="2025-03-30 16:00:00")

                print("Функция запущена успешно!")
                if input("Хотите посмотреть результат? [yes/no]\n") == "yes":
                    print(result)
            except Exception as e:
                print(f"Произошла непредвиденная ошибка! {e}")

        elif command == "3":
            print("Вызываю функцию spending_by_category")
            try:

                transactions = pd.read_excel(file_path)
                result = spending_by_category(transactions=transactions, category="Супермаркеты", date="01.12.2021")

                print("Функция запущена успешно!")
                if input("Хотите посмотреть результат? [yes/no]\n") == "yes":
                    print(result)
            except Exception as e:
                print(f"Произошла непредвиденная ошибка! {e}")

        elif command == "4":
            print("Вызываю функцию cashback_analyze")
            try:

                data = read_xlsx_file(file_path=file_path)
                result = cashback_analyze(data=data, year=2021, month=10)

                print("Функция запущена успешно!")
                if input("Хотите посмотреть результат? [yes/no]\n") == "yes":
                    print(result)
            except Exception as e:
                print(f"Произошла непредвиденная ошибка! {e}")

        elif command == "5":
            print("Вызываю функцию function_to_json")
            try:

                result = function_to_json(greeting, date="2025-03-30 16:00:00")

                print("Функция запущена успешно!")
                if input("Хотите посмотреть результат? [yes/no]\n") == "yes":
                    print(result)
            except Exception as e:
                print(f"Произошла непредвиденная ошибка! {e}")

        elif command == "exit":
            break
