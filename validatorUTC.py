import re

#Части шаблона: год, месяц, день, часы, минуты, секунды
YEAR = r"\d{4}"
MONTH = r"(?:0[1-9]|1[0-2])"
DAY = r"(?:0[1-9]|[12]\d|3[01])"
HOUR = r"(?:[01]\d|2[0-3])"
MINUTE = r"[0-5]\d"
SECOND = r"[0-5]\d"

UTC_PATTERN = f"{YEAR}-{MONTH}-{DAY}T{HOUR}:{MINUTE}:{SECOND}Z"

#Для поиска в тексте время не должно быть приклеено к буквам, цифрам или дефису
#IGNORECASE - буквы T и Z принимаются и заглавными, и строчными
VALIDE_UTC = re.compile(UTC_PATTERN, re.ASCII | re.IGNORECASE)
SEARCH_UTC = re.compile(r"(?<![\w-])" + UTC_PATTERN + r"(?!\w)", re.ASCII | re.IGNORECASE)


def isValidUTC(value: str) -> bool:
    match = VALIDE_UTC.fullmatch(value)
    return match is not None

#Возвращает список всех найденных значений времени
def findUTC(text: str) -> list[str]:
    return SEARCH_UTC.findall(text)
