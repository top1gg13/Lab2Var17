from exceptions.app_error import AppError


# Не удалось подключиться к сайту или сервер не ответил вовремя
class ConnectionFailedError(AppError):
    def __init__(self, url: str):
        self.url = url
        super().__init__(f"Не удалось подключиться к сайту: {url}")
