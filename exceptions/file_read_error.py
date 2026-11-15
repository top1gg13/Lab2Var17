from exceptions.app_error import AppError


# Файл не удалось прочитать: не найден, это папка, нет доступа или не UTF-8
class FileReadError(AppError):
    def __init__(self, path: str, reason: str):
        self.path = path
        super().__init__(f"{reason}: {path}")
