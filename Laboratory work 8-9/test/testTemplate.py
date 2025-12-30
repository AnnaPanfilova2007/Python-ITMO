import unittest
from jinja2 import Environment, PackageLoader, select_autoescape
import models

class TestTemplates(unittest.TestCase):

    def setUp(self):
        # Создаем тестовое окружение
        self.env = Environment(
            loader=PackageLoader("main"),
            autoescape=select_autoescape()
        )

        # Тестовые данные
        self.base_data = {
            'myapp': "Приложение отслеживания курса валют",
            'navigation': [
                {'caption': 'Главная страница', 'href': "/"},
                {'caption': 'Пользователи', 'href': "/users"},
                {'caption': 'Курсы валют', 'href': "/currencies"},
                {'caption': 'Об авторе', 'href': "/author"}
            ],
            'author_name': "Тест",
            'group': "P3121",
            'app_name': "Тест прил",
            'version': "1.0",
        }

    def test_index_template(self):
        """Тест главного шаблона"""
        template = self.env.get_template("main.html")
        result = template.render(**self.base_data)

        # Проверяем основные элементы
        self.assertIn('Тест', result)
        self.assertIn('1.0', result)
        self.assertIn('Главная страница', result)
        self.assertIn('Навигация по сайту', result)

    def test_users_template(self):
        """Тест шаблона пользователей"""


        # Добавляем тестовых пользователей
        test_data = self.base_data.copy()
        test_data['users'] = [
            models.User("Иван Иванов", "ivan@example.com", 1),
            models.User("Анна Смирнова", "anna.s@mail.ru", 2)]

        template = self.env.get_template("users.html")
        result = template.render(**test_data)

        # Проверяем рендеринг списка
        self.assertIn('Иван Иванов', result)
        self.assertIn('Анна Смирнова', result)\

    def test_author_template_variable_passing(self):
        """Тест передачи переменных в шаблон об авторе"""

        # Загружаем шаблон
        template = self.env.get_template("author.html")

        # Рендерим шаблон с базовыми данными
        result = template.render(**self.base_data)

        # Проверяем вывод информации об авторе
        self.assertIn('Тест', result)
        self.assertIn('P3121', result)

    def test_user_template(self):
        """Тест шаблона конкретного пользователя"""
        from models import User, Currency

        # Добавляем тестовые данные
        test_data = self.base_data.copy()
        test_data['user'] = models.User("Иван Иванов", "ivan@example.com", 1)
        test_data['user_currencies'] = [
            models.Currency(1, 840, "USD", "Доллар США", 75.5, 1),
            models.Currency(2, 978, "EUR", "Евро", 89.25, 1)
        ]

        template = self.env.get_template("user_detail.html")
        result = template.render(**test_data)

        # Проверяем рендеринг
        self.assertIn('Иван Иванов', result)
        self.assertIn('USD', result)
        self.assertIn('EUR', result)
        self.assertIn('Доллар США', result)
        self.assertIn('Евро', result)

    def test_currencies_template(self):
        """Тест шаблона валют"""
        from models import Currency

        # Добавляем тестовые валюты
        test_data = self.base_data.copy()
        test_data['currencies'] = [
            Currency(1, 840, "USD", "Доллар США", 75.50, 1),
            Currency(2, 978, "EUR", "Евро", 89.25, 1),
            Currency(3, 392, "JPY", "Японская иена", 0.65, 100)
        ]

        template = self.env.get_template("currencies.html")
        result = template.render(**test_data)

        # Проверяем рендеринг таблицы
        self.assertIn('USD', result)
        self.assertIn('EUR', result)
        self.assertIn('JPY', result)
        self.assertIn('75.5', result)
        self.assertIn('89.25', result)
        self.assertIn('0.65', result)

    def test_author_template(self):
        """Тест шаблона об авторе"""
        template = self.env.get_template("author.html")
        result = template.render(**self.base_data)

        # Проверяем вывод информации об авторе
        self.assertIn('Тест', result)
        self.assertIn('P3121', result)


if __name__ == '__main__':
    unittest.main()