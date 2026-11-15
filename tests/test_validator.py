import unittest

from validatorUTC import isValidUTC, findUTC


class TestIsValidUTC(unittest.TestCase):
    """Проверка строки целиком (isValidUTC)."""

    def test_valid_regular_time(self):
        self.assertTrue(isValidUTC("2026-11-13T16:38:00Z"))

    def test_valid_min_values(self):
        self.assertTrue(isValidUTC("0000-01-01T00:00:00Z"))

    def test_valid_max_values(self):
        self.assertTrue(isValidUTC("9999-12-31T23:59:59Z"))

    def test_invalid_month_13(self):
        self.assertFalse(isValidUTC("2026-13-01T10:00:00Z"))

    def test_invalid_day_32(self):
        self.assertFalse(isValidUTC("2026-11-32T10:00:00Z"))

    def test_invalid_hour_24(self):
        self.assertFalse(isValidUTC("2026-11-13T24:00:00Z"))

    def test_invalid_minute_60(self):
        self.assertFalse(isValidUTC("2026-11-13T16:60:00Z"))

    def test_invalid_second_60(self):
        self.assertFalse(isValidUTC("2026-11-13T16:38:60Z"))

    def test_invalid_without_z(self):
        self.assertFalse(isValidUTC("2026-11-13T16:38:00"))

    def test_valid_lowercase_z_and_t(self):
        self.assertTrue(isValidUTC("2026-11-13T16:38:00z"))
        self.assertTrue(isValidUTC("2026-11-13t16:38:00Z"))
        self.assertTrue(isValidUTC("2026-11-13t16:38:00z"))

    def test_invalid_with_offset(self):
        self.assertFalse(isValidUTC("2026-11-13T19:38:00+03:00"))

    def test_invalid_without_seconds(self):
        self.assertFalse(isValidUTC("2026-11-13T16:38Z"))

    def test_invalid_one_digit_fields(self):
        self.assertFalse(isValidUTC("2026-1-13T16:38:00Z"))
        self.assertFalse(isValidUTC("2026-11-3T6:38:00Z"))

    def test_invalid_five_digit_year(self):
        self.assertFalse(isValidUTC("12026-11-13T16:38:00Z"))

    def test_invalid_extra_text_around(self):
        self.assertFalse(isValidUTC(" 2026-11-13T16:38:00Z"))
        self.assertFalse(isValidUTC("2026-11-13T16:38:00Z abc"))

    def test_invalid_non_ascii_digits(self):
        # Арабско-индийские цифры не должны считаться цифрами (флаг re.ASCII)
        self.assertFalse(isValidUTC("٢٠٢٦-11-13T16:38:00Z"))


class TestFindUTC(unittest.TestCase):
    """Поиск времени в тексте (findUTC)."""

    def test_find_single(self):
        self.assertEqual(findUTC("Старт: 2026-11-13T16:38:00Z"),
                         ["2026-11-13T16:38:00Z"])

    def test_find_multiple_in_order(self):
        text = "a 2026-01-01T00:00:00Z b 2025-12-31T23:59:59Z c"
        self.assertEqual(findUTC(text),
                         ["2026-01-01T00:00:00Z", "2025-12-31T23:59:59Z"])

    def test_find_nothing(self):
        self.assertEqual(findUTC("здесь нет времени"), [])

    def test_find_with_punctuation_around(self):
        text = "(2026-11-13T16:40:16Z), «2026-11-14T00:00:00Z»."
        self.assertEqual(findUTC(text),
                         ["2026-11-13T16:40:16Z", "2026-11-14T00:00:00Z"])

    def test_skip_invalid_values(self):
        text = "2026-11-13T25:00:00Z 2026-13-01T10:00:00Z 2026-11-13T16:38Z"
        self.assertEqual(findUTC(text), [])

    def test_skip_five_digit_year(self):
        self.assertEqual(findUTC("12026-11-13T16:38:00Z"), [])

    def test_skip_glued_letters(self):
        self.assertEqual(findUTC("x2026-11-13T16:38:00Z"), [])
        self.assertEqual(findUTC("2026-11-13T16:38:00Zabc"), [])

    def test_find_lowercase(self):
        self.assertEqual(findUTC("время 2026-11-13t16:38:00z."),
                         ["2026-11-13t16:38:00z"])

    def test_skip_preceded_by_dash(self):
        self.assertEqual(findUTC("-2026-11-13T16:38:00Z"), [])


if __name__ == "__main__":
    unittest.main()
