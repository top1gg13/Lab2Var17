import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock

import requests

from sources import read_file, read_url
from validatorUTC import findUTC
from exceptions import (FileReadError, InvalidUrlError, HttpStatusError,
                        ConnectionFailedError)

SAMPLE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sample.txt")


class TestReadFile(unittest.TestCase):

    def test_read_file_content(self):
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt",
                                         delete=False) as f:
            f.write("Время: 2026-11-13T16:38:00Z")
            path = f.name
        try:
            self.assertEqual(read_file(path), "Время: 2026-11-13T16:38:00Z")
        finally:
            os.remove(path)

    def test_read_empty_file(self):
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as f:
            path = f.name
        try:
            self.assertEqual(read_file(path), "")
        finally:
            os.remove(path)

    def test_read_missing_file_raises(self):
        with self.assertRaises(FileReadError) as context:
            read_file("no_such_file_12345.txt")
        self.assertIn("Файл не найден", str(context.exception))

    def test_read_directory_raises(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(FileReadError):
                read_file(folder)

    def test_read_not_utf8_raises(self):
        with tempfile.NamedTemporaryFile("wb", delete=False) as f:
            f.write(b"\xff\xfe\xfa")
            path = f.name
        try:
            with self.assertRaises(FileReadError) as context:
                read_file(path)
            self.assertIn("UTF-8", str(context.exception))
        finally:
            os.remove(path)

    def test_sample_file_finds_only_valid(self):
        found = findUTC(read_file(SAMPLE))
        self.assertEqual(found, [
            "2026-11-13T16:38:00Z",
            "2026-11-13T16:40:15Z",
            "2026-11-13T16:40:16Z",
            "2026-11-14T00:00:00Z",
        ])


class TestReadUrl(unittest.TestCase):

    @patch("sources.requests.get")
    def test_read_url_returns_text(self, mock_get):
        mock_get.return_value = MagicMock(text="<p>2026-11-13T16:38:00Z</p>")
        with patch("builtins.print"):
            result = read_url("https://example.com")
        self.assertEqual(result, "<p>2026-11-13T16:38:00Z</p>")
        mock_get.assert_called_once_with("https://example.com", timeout=10)

    @patch("sources.requests.get")
    def test_read_url_http_error(self, mock_get):
        response = MagicMock()
        response.raise_for_status.side_effect = requests.HTTPError(
            response=MagicMock(status_code=404))
        mock_get.return_value = response
        with self.assertRaises(HttpStatusError) as context:
            read_url("https://example.com/404")
        self.assertEqual(context.exception.status_code, 404)

    @patch("sources.requests.get")
    def test_read_url_connection_error(self, mock_get):
        mock_get.side_effect = requests.ConnectionError()
        with self.assertRaises(ConnectionFailedError):
            read_url("https://unreachable.invalid")

    @patch("sources.requests.get")
    def test_read_url_timeout(self, mock_get):
        mock_get.side_effect = requests.Timeout()
        with self.assertRaises(ConnectionFailedError):
            read_url("https://slow.example.com")

    def test_read_url_without_scheme(self):
        # requests сам отклоняет URL без http:// ещё до запроса в сеть
        with self.assertRaises(InvalidUrlError):
            read_url("example.com")


if __name__ == "__main__":
    unittest.main()
