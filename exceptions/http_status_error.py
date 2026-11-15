from exceptions.app_error import AppError


# Сервер ответил кодом ошибки (404, 500 и т.д.)
class HttpStatusError(AppError):
    def __init__(self, status_code):
        self.status_code = status_code
        super().__init__(f"Сервер вернул ошибку: {status_code}")
