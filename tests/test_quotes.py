import unittest
from pathlib import Path
from unittest.mock import patch
import tempfile
import os


# Подменяем DATA_FILE на временный файл перед импортом модуля
class TestQuotes(unittest.TestCase):

    def setUp(self):
        """Создаем временный файл для каждого теста."""
        self.tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        )
        self.tmp.close()
        # Патчим путь к файлу в модуле quotes
        self.patcher = patch("src.quotes.DATA_FILE", Path(self.tmp.name))
        self.patcher.start()

    def tearDown(self):
        """Удаляем временный файл после каждого теста."""
        self.patcher.stop()
        os.unlink(self.tmp.name)

    def test_empty_file_returns_none(self):
        from src.quotes import get_random_quote
        self.assertIsNone(get_random_quote())

    def test_empty_file_count_is_zero(self):
        from src.quotes import count_quotes
        self.assertEqual(count_quotes(), 0)

    def test_add_and_count(self):
        from src.quotes import add_quote, count_quotes
        add_quote("Первая цитата")
        add_quote("Вторая цитата")
        self.assertEqual(count_quotes(), 2)

    def test_add_returns_true_for_new_quote(self):
        from src.quotes import add_quote
        result = add_quote("Новая цитата")
        self.assertTrue(result)

    def test_add_returns_false_for_duplicate(self):
        from src.quotes import add_quote
        add_quote("Дубликат")
        result = add_quote("Дубликат")
        self.assertFalse(result)

    def test_get_random_returns_string(self):
        from src.quotes import add_quote, get_random_quote
        add_quote("Тестовая цитата")
        quote = get_random_quote()
        self.assertIsInstance(quote, str)
        self.assertEqual(quote, "Тестовая цитата")


if __name__ == "__main__":
    unittest.main()
