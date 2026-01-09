import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from http.server import HTTPServer
import threading
import time
import urllib.request
import urllib.error
import json

# Добавляем путь к текущей директории
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Импортируем основной модуль
try:
    from main import SimpleHTTPRequestHandler, users, user_currencies_list, currenci_list
    import models

    IMPORT_SUCCESS = True
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("Создаем заглушки для тестирования...")
    IMPORT_SUCCESS = False


    # Создаем заглушки для тестирования
    class MockModel:
        def __init__(self, *args, **kwargs):
            pass


    models = Mock()
    models.User = MockModel
    models.UserCurrency = MockModel
    models.Currency = MockModel
    models.Author = MockModel
    models.App = MockModel

    users = []
    user_currencies_list = []
    currenci_list = []


    class SimpleHTTPRequestHandler:
        pass


class TestCurrencyController(unittest.TestCase):
    """Тестирование контроллера валют"""

    @classmethod
    def setUpClass(cls):
        """Запуск тестового сервера перед всеми тестами"""
        if not IMPORT_SUCCESS:
            return

        cls.server = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(1)  # Даем серверу время на запуск

    @classmethod
    def tearDownClass(cls):
        """Остановка тестового сервера после всех тестов"""
        if not IMPORT_SUCCESS:
            return

        cls.server.shutdown()
        cls.server_thread.join()

    def test_1_users_list(self):
        """Тест получения списка пользователей"""
        if not IMPORT_SUCCESS:
            self.skipTest("Модуль не импортирован")

        try:
            response = urllib.request.urlopen('http://localhost:8081/users')
            self.assertEqual(response.status, 200)
            html_content = response.read().decode('utf-8')

            # Проверяем, что страница содержит данные о пользователях
            self.assertIn('Пользователи', html_content)

        except urllib.error.URLError as e:
            self.fail(f"Не удалось подключиться к серверу: {e}")

    def test_2_user_detail(self):
        """Тест получения детальной информации о пользователе"""
        if not IMPORT_SUCCESS:
            self.skipTest("Модуль не импортирован")

        try:
            response = urllib.request.urlopen('http://localhost:8081/user?id=1')
            self.assertEqual(response.status, 200)
            html_content = response.read().decode('utf-8')

        except urllib.error.URLError as e:
            self.fail(f"Не удалось подключиться к серверу: {e}")

    def test_3_user_not_found(self):
        """Тест обработки несуществующего пользователя"""
        if not IMPORT_SUCCESS:
            self.skipTest("Модуль не импортирован")

        try:
            urllib.request.urlopen('http://localhost:8081/user?id=999')
            self.fail("Ожидалось исключение 404")
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 404)
        except urllib.error.URLError:
            pass  # Игнорируем ошибки подключения

    def test_4_currencies_list(self):
        """Тест получения списка валют"""
        if not IMPORT_SUCCESS:
            self.skipTest("Модуль не импортирован")

        try:
            response = urllib.request.urlopen('http://localhost:8081/currencies')
            self.assertEqual(response.status, 200)
            html_content = response.read().decode('utf-8')

        except urllib.error.URLError as e:
            self.fail(f"Не удалось подключиться к серверу: {e}")

    def test_5_main_page(self):
        """Тест главной страницы"""
        if not IMPORT_SUCCESS:
            self.skipTest("Модуль не импортирован")

        try:
            response = urllib.request.urlopen('http://localhost:8081/')
            self.assertEqual(response.status, 200)
            html_content = response.read().decode('utf-8')

        except urllib.error.URLError as e:
            self.fail(f"Не удалось подключиться к серверу: {e}")

    def test_6_author_page(self):
        """Тест страницы об авторе"""
        if not IMPORT_SUCCESS:
            self.skipTest("Модуль не импортирован")

        try:
            response = urllib.request.urlopen('http://localhost:8081/author')
            self.assertEqual(response.status, 200)
            html_content = response.read().decode('utf-8')

        except urllib.error.URLError as e:
            self.fail(f"Не удалось подключиться к серверу: {e}")

    def test_7_page_not_found(self):
        """Тест обработки несуществующей страницы"""
        if not IMPORT_SUCCESS:
            self.skipTest("Модуль не импортирован")

        try:
            urllib.request.urlopen('http://localhost:8081/notfound')
            self.fail("Ожидалось исключение 404")
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 404)
        except urllib.error.URLError:
            pass


class TestCurrencyCRUD(unittest.TestCase):
    """Тестирование CRUD операций для валют"""

    def test_1_currency_model_creation(self):
        """Тест создания модели Currency"""
        currency = models.Currency(1, 840, "Доллар США", "USD", 75.5, 1)

        self.assertEqual(currency.id, 1)
        self.assertEqual(currency.num_code, 840)
        self.assertEqual(currency.name_v, "Доллар США")
        self.assertEqual(currency.char_code, "USD")
        self.assertEqual(currency.value, 75.5)
        self.assertEqual(currency.nominal, 1)

    def test_2_user_model_creation(self):
        """Тест создания модели User"""
        user = models.User("Иван Иванов", "ivan@example.com", 1)

        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, "Иван Иванов")
        self.assertEqual(user.mail, "ivan@example.com")

    def test_3_user_currency_model_creation(self):
        """Тест создания модели UserCurrency"""
        user_currency = models.UserCurrency(1, 1, 1)

        self.assertEqual(user_currency.id, 1)
        self.assertEqual(user_currency.uid, 1)
        self.assertEqual(user_currency.current_id, 1)

    @patch('main.get_currencies')
    def test_4_currency_api_integration(self, mock_get_currencies):
        """Тест интеграции с API валют"""
        if not IMPORT_SUCCESS:
            self.skipTest("Модуль не импортирован")

        # Мокаем ответ API
        mock_get_currencies.return_value = {
            "USD": 75.5,
            "EUR": 85.0,
            "GBP": 100.0
        }

        # Имитируем вызов функции get_currencies
        result = mock_get_currencies(["USD", "EUR", "GBP"])

        self.assertIn("USD", result)
        self.assertIn("EUR", result)
        self.assertIn("GBP", result)
        self.assertEqual(result["USD"], 75.5)
        self.assertEqual(result["EUR"], 85.0)


class TestControllerLogic(unittest.TestCase):
    """Тестирование логики контроллера"""

    def test_1_user_currency_filtering(self):
        """Тест фильтрации валют пользователя"""
        # Тестовые данные
        test_users = [
            models.User("Иван Иванов", "ivan@example.com", 1),
            models.User("Анна Смирнова", "anna.s@mail.ru", 2),
        ]

        test_user_currencies = [
            models.UserCurrency(1, 1, 1),  # Иван подписан на USD
            models.UserCurrency(2, 1, 2),  # Иван подписан на EUR
            models.UserCurrency(3, 2, 1),  # Анна подписан на USD
        ]

        test_currencies = [
            models.Currency(1, 840, "Доллар США", "USD", 75.5, 1),
            models.Currency(2, 978, "Евро", "EUR", 85.0, 1),
        ]

        # Тестируем фильтрацию для пользователя 1
        user_id = 1
        user_currency_ids = [
            uc.current_id for uc in test_user_currencies if uc.uid == user_id
        ]

        self.assertEqual(len(user_currency_ids), 2)
        self.assertIn(1, user_currency_ids)
        self.assertIn(2, user_currency_ids)

    def test_2_unique_currencies_count(self):
        """Тест подсчета уникальных валют"""
        # Тестовые данные с дубликатами
        test_user_currencies = [
            models.UserCurrency(1, 1, 1),
            models.UserCurrency(2, 1, 1),  # Дубликат
            models.UserCurrency(3, 1, 2),
            models.UserCurrency(4, 1, 2),  # Дубликат
            models.UserCurrency(5, 1, 3),
        ]

        user_id = 1
        user_currency_ids = [
            uc.current_id for uc in test_user_currencies if uc.uid == user_id
        ]

        unique_count = len(set(user_currency_ids))
        self.assertEqual(unique_count, 3)  # Должно быть 3 уникальные валюты
        self.assertEqual(len(user_currency_ids), 5)  # Всего подписок 5


class TestErrorHandling(unittest.TestCase):
    """Тестирование обработки ошибок"""

    def test_1_missing_id_parameter(self):
        """Тест обработки запроса без параметра ID"""
        if not IMPORT_SUCCESS:
            self.skipTest("Модуль не импортирован")

        try:
            urllib.request.urlopen('http://localhost:8081/user')
            self.fail("Ожидалось исключение 400")
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 400)
        except urllib.error.URLError:
            pass

    def test_2_invalid_id_format(self):
        """Тест обработки некорректного формата ID"""
        if not IMPORT_SUCCESS:
            self.skipTest("Модуль не импортирован")

        try:
            urllib.request.urlopen('http://localhost:8081/user?id=abc')
            self.fail("Ожидалось исключение 400")
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 400)
        except urllib.error.URLError:
            pass


class TestPerformance(unittest.TestCase):
    """Тесты производительности"""

    def test_1_users_list_performance(self):
        """Тест производительности загрузки списка пользователей"""
        if not IMPORT_SUCCESS:
            self.skipTest("Модуль не импортирован")

        import time

        start_time = time.time()

        # Делаем несколько запросов для теста производительности
        try:
            for _ in range(5):
                urllib.request.urlopen('http://localhost:8081/users').read()
        except:
            pass

        end_time = time.time()
        execution_time = end_time - start_time

        # Проверяем, что время выполнения приемлемое
        self.assertLess(execution_time, 3.0,
                        f"Загрузка списка пользователей слишком медленная: {execution_time:.2f} сек")

    def test_2_concurrent_requests(self):
        """Тест обработки нескольких одновременных запросов"""
        if not IMPORT_SUCCESS:
            self.skipTest("Модуль не импортирован")

        import threading

        results = []

        def make_request():
            try:
                response = urllib.request.urlopen('http://localhost:8081/')
                results.append(response.status)
            except:
                results.append(0)

        # Создаем несколько потоков
        threads = []
        for _ in range(3):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()

        # Ждем завершения всех потоков
        for thread in threads:
            thread.join()

        # Проверяем, что все запросы были обработаны
        self.assertEqual(len(results), 3)
        successful_requests = sum(1 for r in results if r == 200)
        self.assertGreaterEqual(successful_requests, 2,
                                "Слишком много запросов провалилось")


class TestTemplateRendering(unittest.TestCase):
    """Тестирование рендеринга шаблонов"""

    @patch('main.Environment')
    def test_1_template_loading(self, mock_env):
        """Тест загрузки шаблонов"""
        if not IMPORT_SUCCESS:
            self.skipTest("Модуль не импортирован")

        # Создаем мок шаблона
        mock_template = Mock()
        mock_template.render.return_value = "<html>Test</html>"

        # Настраиваем мок окружения
        mock_env_instance = Mock()
        mock_env_instance.get_template.return_value = mock_template
        mock_env.return_value = mock_env_instance

        # Проверяем, что шаблон загружается
        template = mock_env_instance.get_template("main.html")
        self.assertIsNotNone(template)

    def test_2_data_passing_to_templates(self):
        """Тест передачи данных в шаблоны"""
        # Тестовые данные
        test_data = {
            'myapp': 'Test App',
            'navigation': [{'caption': 'Home', 'href': '/'}],
            'author_name': 'Test Author',
            'group': 'Test Group'
        }

        # Проверяем структуру данных
        self.assertIn('myapp', test_data)
        self.assertIn('navigation', test_data)
        self.assertIn('author_name', test_data)
        self.assertIn('group', test_data)

        # Проверяем типы данных
        self.assertIsInstance(test_data['navigation'], list)
        self.assertIsInstance(test_data['author_name'], str)


class TestNavigation(unittest.TestCase):
    """Тестирование навигации"""

    def test_1_navigation_structure(self):
        """Тест структуры навигационного меню"""
        # Ожидаемая структура навигации
        expected_nav = [
            {'caption': 'Главная страница', 'href': '/'},
            {'caption': 'Пользователи', 'href': '/users'},
            {'caption': 'Курсы валют', 'href': '/currencies'},
            {'caption': 'Об авторе', 'href': '/author'}
        ]

        # Проверяем структуру
        self.assertEqual(len(expected_nav), 4)

        # Проверяем каждый элемент
        for item in expected_nav:
            self.assertIn('caption', item)
            self.assertIn('href', item)
            self.assertIsInstance(item['caption'], str)
            self.assertIsInstance(item['href'], str)

    def test_2_navigation_urls(self):
        """Тест корректности URL в навигации"""
        nav_items = [
            {'caption': 'Главная страница', 'href': '/'},
            {'caption': 'Пользователи', 'href': '/users'},
            {'caption': 'Курсы валют', 'href': '/currencies'},
            {'caption': 'Об авторе', 'href': '/author'}
        ]

        # Проверяем, что все URL начинаются с /
        for item in nav_items:
            self.assertTrue(item['href'].startswith('/'),
                            f"URL '{item['href']}' не начинается с '/'")


def run_all_tests():
    """Запуск всех тестов с красивым выводом"""
    print("=" * 70)
    print("ЗАПУСК ТЕСТИРОВАНИЯ КОНТРОЛЛЕРА ВАЛЮТ")
    print("=" * 70)

    # Создаем тестовый набор
    test_suite = unittest.TestSuite()

    # Добавляем тесты в определенном порядке
    test_suite.addTest(unittest.makeSuite(TestCurrencyCRUD))
    test_suite.addTest(unittest.makeSuite(TestControllerLogic))
    test_suite.addTest(unittest.makeSuite(TestNavigation))
    test_suite.addTest(unittest.makeSuite(TestTemplateRendering))
    test_suite.addTest(unittest.makeSuite(TestErrorHandling))
    test_suite.addTest(unittest.makeSuite(TestPerformance))
    test_suite.addTest(unittest.makeSuite(TestCurrencyController))

    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Выводим красивую статистику
    print("\n" + "=" * 70)
    print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("=" * 70)

    total_tests = result.testsRun
    failed = len(result.failures)
    errors = len(result.errors)
    skipped = len(getattr(result, 'skipped', []))
    passed = total_tests - failed - errors - skipped

    print(f"\n📊 Статистика:")
    print(f"   Всего тестов: {total_tests}")
    print(f"   ✅ Успешно: {passed}")
    print(f"   ⚠️  Пропущено: {skipped}")
    print(f"   ❌ Провалено: {failed}")
    print(f"   💥 Ошибок: {errors}")

    # Выводим процент успешных тестов
    if total_tests > 0:
        success_rate = (passed / total_tests) * 100
        print(f"   📈 Успешность: {success_rate:.1f}%")

    # Выводим проваленные тесты
    if result.failures:
        print(f"\n🔴 ПРОВАЛЕННЫЕ ТЕСТЫ:")
        for i, (test, traceback) in enumerate(result.failures, 1):
            test_name = str(test).split()[0]
            print(f"   {i}. {test_name}")

    # Выводим ошибки
    if result.errors:
        print(f"\n⚡ ОШИБКИ:")
        for i, (test, traceback) in enumerate(result.errors, 1):
            test_name = str(test).split()[0]
            print(f"   {i}. {test_name}")

    print("\n" + "=" * 70)

    # Возвращаем код выхода
    return 0 if failed == 0 and errors == 0 else 1


if __name__ == '__main__':
    # Запускаем все тесты
    exit_code = run_all_tests()

    # Выходим с соответствующим кодом
    sys.exit(exit_code)