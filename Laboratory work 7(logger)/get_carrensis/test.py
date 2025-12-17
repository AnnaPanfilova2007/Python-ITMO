import unittest
import io

import requests

from main import get_currencies
from decorator import logger


class TestGetCurrenciesApi(unittest.TestCase):
    """
       Тестирование работы API для получения курсов валют.

       Тесты проверяют корректность взаимодействия с внешним API
       через функцию get_currencies.
    """
    def test_basic(self):
        lst = ['AUD', 'AZN', 'DZD']
        curs = get_currencies(lst)
        for item in lst:
            self.assertIn(item, curs)
            self.assertTrue(isinstance(curs[item], int | float))

    def test_raises(self):
        with self.assertRaises(
                requests.exceptions.ConnectionError):
            get_currencies(['USD', 'EUR', 'GBP'], url="http://")

        with self.assertRaises(KeyError):
            get_currencies(["Валюта отсутствует в данных"])


def power(a: int, b: int) -> int:
    """
    Вычисляет a в степени b для целых чисел.

    Параметры
    ---------
    a : int
        Основание степени.
    b : int
        Показатель степени.

    Возвращает
    ----------
    int
        Результат a в степени b.

    Исключения
    ----------
    TypeError
        Если a или b не являются целыми числами.
    """
    if not isinstance(b, int):
        raise TypeError(f"Некорректное значение {b}")
    if not isinstance(a, int):
        raise TypeError(f"Некорректное значение {a}")
    if b == 0:
        return 1
    if b % 2 == 0:
        return power(a, b // 2) ** 2
    return power(a, b - 1) * a


class TestLogger(unittest.TestCase):
    """
        Тестирование декоратора логирования.\
    """

    def setUp(self):
        """
        Prepares inner variables for testing
        """
        self.stream = io.StringIO()
        self.trace = logger(power, handle=self.stream)

    def test_basic(self):
        self.trace(2, 10)
        self.assertIn("Вызов функции", self.stream.getvalue())
        self.assertIn("выполнена без исключений", self.stream.getvalue())

    def test_raises1(self):
        with self.assertRaises(TypeError):
            self.trace(19.5, 6)
            self.assertIn("Некорректное значение: 19.5", self.stream.getvalue())

    def test_raises2(self):
        with self.assertRaises(TypeError):
            self.trace(6, "19")
            self.assertIn("Некорректное значение '19'", self.stream.getvalue())




    def tearDown(self):
        """
        Cancels resources
        """
        del self.stream


class TestStreamWrite(unittest.TestCase):
    """
    Tests whether the logging decorator works or not
    when it's provided with a resource
    """

    def setUp(self):
        """
        Prepares inner variables for testing
        """
        self.nonStandardStream = io.StringIO()
        self.trace = logger(get_currencies, handle=self.nonStandardStream)

    def test_writing_stream(self):
        with self.assertRaises(requests.exceptions.RequestException):
            self.get_currencies = self.trace(
                ['USD'],
                url="https://"
            )
            self.assertIn('совершена с исключением', self.nonStandardStream.getvalue())


    def tearDown(self):
        """
        Cancels the resources
        """
        del self.nonStandardStream


if __name__ == "__main__":
    unittest.main(verbosity=2)