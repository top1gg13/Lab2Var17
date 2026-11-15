from exceptions.app_error import AppError


# Строка не является корректным URL (например, нет http:// или https://)
class InvalidUrlError(AppError):
    def __init__(self, url: str):
        self.url = url
        super().__init__(f"Некорректный URL: {url}")
