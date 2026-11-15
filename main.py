import requests

from validatorUTC import isValidUTC, findUTC
from sources import read_file, read_url
from exceptions import AppError

def check_UTC() -> None:
    #Проверка корректности времени в формате UTC
    timeUTC = input("Введите время в формате UTC: ").strip()
    if isValidUTC(timeUTC):
        print(f"Время корректно.")
    else:
        print("Введено некорректное время.")

def search_text() -> None:
    #Поиск времени во введённом пользователем тексте
    text = input("Введите текст: ")
    show_results(findUTC(text))

def show_results(found: list[str]) -> None:
    #Вывод найденных значений, каждое с новой строки
    if not found:
        print("Ничего не найдено.")
    for i in found:
        print(i)

def search_file() -> None:
    path = input("Введите путь к фалйу: ").strip()
    try:
        show_results(findUTC(read_file(path)))
    except AppError as error:
        print(error)

def search_url() -> None:
    url = input("Введите URL: ").strip()
    try:
        show_results(findUTC(read_url(url)))
    except AppError as error:
        print(error)


def main():
    #Главное меню программы
    while True:
        print("\n=== Проверка и поиск синтаксически корректного времени в формате UTC ===")
        print("1. Проверка времени в формате UTC")
        print("2. Найти время во введённом тексте")
        print("3. Найти время в файле")
        print("4. Найти время на веб-странице")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()
        if choice == "1":
            check_UTC()
        elif choice == "2":
            search_text()
        elif choice == "3":
            search_file()
        elif choice == "4":
            search_url()
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Выберите пункт от 0 до 2.")

if __name__ == "__main__":
    main()
