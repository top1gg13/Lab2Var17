# Собственные исключения программы, по одному файлу на каждый случай
from exceptions.app_error import AppError
from exceptions.file_read_error import FileReadError
from exceptions.invalid_url_error import InvalidUrlError
from exceptions.http_status_error import HttpStatusError
from exceptions.connection_failed_error import ConnectionFailedError

__all__ = [
    "AppError",
    "FileReadError",
    "InvalidUrlError",
    "HttpStatusError",
    "ConnectionFailedError",
]
