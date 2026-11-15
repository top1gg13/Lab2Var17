import re
import requests

from validatorUTC import findUTC
from exceptions import (FileReadError, InvalidUrlError, HttpStatusError,
                        ConnectionFailedError)

#Чтение текста из файла
def read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise FileReadError(path, "Файл не найден")
    except UnicodeDecodeError:
        raise FileReadError(path, "Файл не в кодировке UTF-8")
    except OSError:
        raise FileReadError(path, "Не удалось прочитать файл")

#Загрузка текста веб-страницы
def read_url(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise HttpStatusError(error.response.status_code)
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        raise ConnectionFailedError(url)
    except requests.exceptions.RequestException:
        raise InvalidUrlError(url)
    return response.text
