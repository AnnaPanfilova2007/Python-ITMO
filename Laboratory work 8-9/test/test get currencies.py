import unittest
import sys
from unittest.mock import patch, Mock
import io
import requests
from requests.exceptions import RequestException, ConnectionError
from utilits.currencies_api import get_currencies


class TestGetCurrencies(unittest.TestCase):

    def setUp(self):
        """Настройка тестовых данных"""
        self.test_currencies = ["USD", "EUR", "GBP"]
        self.test_url = "https://www.cbr-xml-daily.ru/daily_json.js"
        self.test_output = io.StringIO()

        # Пример корректного ответа API
        self.valid_response_data = {
            "Valute": {
                "USD": {"Value": 75.5, "Previous": 75.0},
                "EUR": {"Value": 85.0, "Previous": 84.5},
                "GBP": {"Value": 95.0, "Previous": 94.5},
                "JPY": {"Value": 0.65, "Previous": 0.64}
            }
        }

        # Ответ с отсутствующими валютами
        self.partial_response_data = {
            "Valute": {
                "USD": {"Value": 75.5, "Previous": 75.0},
                "EUR": {"Value": 85.0, "Previous": 84.5}
                # GBP отсутствует
            }
        }

        # Ответ без ключа Valute
        self.invalid_structure_data = {
            "Currency": {
                "USD": {"Value": 75.5}
            }
        }

        # Ответ с некорректным типом данных
        self.invalid_type_data = {
            "Valute": {
                "USD": {"Value": "не число", "Previous": 75.0}
            }
        }

        # Ответ с невалидным JSON
        self.invalid_json = "{invalid json}"

    def tearDown(self):
        """Очистка после тестов"""
        self.test_output.close()

    def test_successful_response_with_valid_currencies(self):
        """Тест успешного получения курсов валют"""
        mock_response = Mock()
        mock_response.json.return_value = self.valid_response_data
        mock_response.raise_for_status.return_value = None

        with patch('requests.get', return_value=mock_response):
            result = get_currencies(self.test_currencies, self.test_url, self.test_output)

            self.assertEqual(len(result), 3)
            self.assertIn("USD", result)
            self.assertIn("EUR", result)
            self.assertIn("GBP", result)
            self.assertEqual(result["USD"], 75.5)
            self.assertEqual(result["EUR"], 85.0)
            self.assertEqual(result["GBP"], 95.0)

    def test_single_currency_request(self):
        """Тест запроса одной валюты"""
        mock_response = Mock()
        mock_response.json.return_value = self.valid_response_data
        mock_response.raise_for_status.return_value = None

        with patch('requests.get', return_value=mock_response):
            result = get_currencies(["USD"], self.test_url, self.test_output)

            self.assertEqual(len(result), 1)
            self.assertEqual(result["USD"], 75.5)

    def test_empty_currency_list(self):
        """Тест с пустым списком валют"""
        mock_response = Mock()
        mock_response.json.return_value = self.valid_response_data
        mock_response.raise_for_status.return_value = None

        with patch('requests.get', return_value=mock_response):
            result = get_currencies([], self.test_url, self.test_output)

            self.assertEqual(result, {})

    def test_currency_not_found(self):
        """Тест обработки отсутствующей валюты"""
        mock_response = Mock()
        mock_response.json.return_value = self.partial_response_data
        mock_response.raise_for_status.return_value = None

        with patch('requests.get', return_value=mock_response):
            with self.assertRaises(KeyError):
                get_currencies(self.test_currencies, self.test_url, self.test_output)

    def test_invalid_json_response(self):
        """Тест обработки некорректного JSON"""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = ValueError("Invalid JSON")

        with patch('requests.get', return_value=mock_response):
            with self.assertRaises(ValueError) as context:
                get_currencies(self.test_currencies, self.test_url, self.test_output)
            self.assertIn("Некорректный JSON", str(context.exception))

    def test_missing_valute_key(self):
        """Тест ответа без ключа Valute"""
        mock_response = Mock()
        mock_response.json.return_value = self.invalid_structure_data
        mock_response.raise_for_status.return_value = None

        with patch('requests.get', return_value=mock_response):
            with self.assertRaises(KeyError) as context:
                get_currencies(self.test_currencies, self.test_url, self.test_output)
            self.assertIn("Нет ключа 'Valute'", str(context.exception))

    def test_invalid_currency_value_type(self):
        """Тест некорректного типа данных курса валюты"""
        mock_response = Mock()
        mock_response.json.return_value = self.invalid_type_data
        mock_response.raise_for_status.return_value = None

        with patch('requests.get', return_value=mock_response):
            with self.assertRaises(TypeError) as context:
                get_currencies(["USD"], self.test_url, self.test_output)
            self.assertIn("Курс валюты имеет неверный тип", str(context.exception))

    def test_http_error(self):
        """Тест обработки HTTP ошибки"""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = RequestException("HTTP Error")

        with patch('requests.get', return_value=mock_response):
            with self.assertRaises(ConnectionError) as context:
                get_currencies(self.test_currencies, self.test_url, self.test_output)
            self.assertIn("Упали с исключением", str(context.exception))

    def test_network_connection_error(self):
        """Тест ошибки сетевого соединения"""
        with patch('requests.get', side_effect=ConnectionError("Network error")):
            with self.assertRaises(ConnectionError) as context:
                get_currencies(self.test_currencies, self.test_url, self.test_output)
            self.assertIn("Упали с исключением", str(context.exception))

    def test_timeout_error(self):
        """Тест ошибки таймаута"""
        with patch('requests.get', side_effect=requests.exceptions.Timeout("Timeout")):
            with self.assertRaises(ConnectionError) as context:
                get_currencies(self.test_currencies, self.test_url, self.test_output)

    def test_output_handle_usage(self):
        """Тест использования переданного handle для вывода ошибок"""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = RequestException("Test error")

        output = io.StringIO()

        with patch('requests.get', return_value=mock_response):
            try:
                get_currencies(self.test_currencies, self.test_url, output)
            except ConnectionError:
                pass

        output_value = output.getvalue()
        self.assertIn("Ошибка при запросе к API", output_value)
        self.assertIn("Test error", output_value)

    def test_different_url(self):
        """Тест с другим URL"""
        custom_url = "https://custom-api.example.com/currencies"
        mock_response = Mock()
        mock_response.json.return_value = self.valid_response_data
        mock_response.raise_for_status.return_value = None

        with patch('requests.get', return_value=mock_response) as mock_get:
            result = get_currencies(["USD"], custom_url, self.test_output)

            mock_get.assert_called_once_with(custom_url)
            self.assertEqual(result["USD"], 75.5)

    def test_float_conversion(self):
        """Тест корректности конвертации в float"""
        mock_response = Mock()
        mock_response.json.return_value = self.valid_response_data
        mock_response.raise_for_status.return_value = None

        with patch('requests.get', return_value=mock_response):
            result = get_currencies(["USD", "JPY"], self.test_url, self.test_output)

            self.assertIsInstance(result["USD"], float)
            self.assertIsInstance(result["JPY"], float)
            self.assertEqual(result["USD"], 75.5)
            self.assertEqual(result["JPY"], 0.65)


class TestIntegrationGetCurrencies(unittest.TestCase):
    """Интеграционные тесты (требуют реального подключения к интернету)"""

    def setUp(self):
        self.test_currencies = ["USD", "EUR"]
        self.test_url = "https://www.cbr-xml-daily.ru/daily_json.js"

    @unittest.skipUnless(
        sys.version_info >= (3, 6),
        "Требуется Python 3.6+ для интеграционных тестов"
    )
    def test_real_api_connection(self):
        """Тест реального подключения к API (опционально, может пропускаться)"""
        try:
            result = get_currencies(self.test_currencies, self.test_url)
            self.assertIsInstance(result, dict)
            if "USD" in result and "EUR" in result:
                self.assertIsInstance(result["USD"], float)
                self.assertIsInstance(result["EUR"], float)
                self.assertGreater(result["USD"], 0)
                self.assertGreater(result["EUR"], 0)
        except RequestException:
            self.skipTest("Нет подключения к интернету или API недоступно")


if __name__ == '__main__':
    # Запуск тестов
    unittest.main(verbosity=2)