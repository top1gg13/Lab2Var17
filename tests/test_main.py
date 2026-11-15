import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import main
from exceptions import FileReadError, HttpStatusError


def run(func, inputs):
    out = io.StringIO()
    with patch("builtins.input", side_effect=inputs), redirect_stdout(out):
        func()
    return out.getvalue()


class TestMainFunctions(unittest.TestCase):

    def test_check_utc_valid(self):
        self.assertIn("Время корректно", run(main.check_UTC, ["2026-11-13T16:38:00Z"]))

    def test_check_utc_invalid(self):
        self.assertIn("некорректное", run(main.check_UTC, ["2026-11-13T24:00:00Z"]))

    def test_show_results_empty(self):
        out = io.StringIO()
        with redirect_stdout(out):
            main.show_results([])
        self.assertIn("Ничего не найдено", out.getvalue())

    def test_show_results_prints_each(self):
        out = io.StringIO()
        with redirect_stdout(out):
            main.show_results(["2026-11-13T16:38:00Z", "2026-11-14T00:00:00Z"])
        self.assertEqual(out.getvalue().splitlines(),
                         ["2026-11-13T16:38:00Z", "2026-11-14T00:00:00Z"])

    def test_search_text(self):
        out = run(main.search_text, ["лог 2026-11-13T16:38:00Z конец"])
        self.assertIn("2026-11-13T16:38:00Z", out)

    @patch("main.read_file", return_value="x 2026-11-14T00:00:00Z y")
    def test_search_file(self, mock_read):
        out = run(main.search_file, [" data.txt "])
        mock_read.assert_called_once_with("data.txt")
        self.assertIn("2026-11-14T00:00:00Z", out)

    @patch("main.read_file",
           side_effect=FileReadError("a.txt", "Файл не найден"))
    def test_search_file_error_message(self, _):
        out = run(main.search_file, ["a.txt"])
        self.assertIn("Файл не найден: a.txt", out)

    @patch("main.read_url", side_effect=HttpStatusError(404))
    def test_search_url_error_message(self, _):
        out = run(main.search_url, ["https://example.com/x"])
        self.assertIn("404", out)

    @patch("main.read_url", return_value="<b>нет времени</b>")
    def test_search_url_nothing(self, mock_read):
        out = run(main.search_url, ["https://example.com"])
        mock_read.assert_called_once_with("https://example.com")
        self.assertIn("Ничего не найдено", out)


class TestMenu(unittest.TestCase):

    def test_exit(self):
        self.assertIn("До свидания", run(main.main, ["0"]))

    def test_unknown_choice_then_exit(self):
        out = run(main.main, ["9", "0"])
        self.assertIn("Выберите пункт", out)
        self.assertIn("До свидания", out)

    def test_menu_option_1(self):
        out = run(main.main, ["1", "2026-11-13T16:38:00Z", "0"])
        self.assertIn("Время корректно", out)

    @patch("main.search_file")
    def test_menu_option_3_calls_search_file(self, mock_search):
        run(main.main, ["3", "0"])
        mock_search.assert_called_once()

    @patch("main.search_url")
    def test_menu_option_4_calls_search_url(self, mock_search):
        run(main.main, ["4", "0"])
        mock_search.assert_called_once()


if __name__ == "__main__":
    unittest.main()
