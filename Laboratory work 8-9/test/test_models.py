import unittest
# Импортируем все тестируемые классы из модуля models
from models import Author, App, User, Currency, UserCurrency


class TestAuthor(unittest.TestCase):
    """
    Тестирование класса Author (Автор).
    Проверяет корректность работы инициализации, геттеров и сеттеров.
    """

    def setUp(self):
        """
        Метод, выполняемый перед каждым тестом.
        Создает экземпляр Author для тестирования.
        """
        self.author = Author("Имя", "P3121", "http:/.../")

    def test_initialization(self):
        """
        Проверяет, что значения корректно устанавливаются при создании.
        """
        self.assertEqual(self.author.name, "Имя")
        self.assertEqual(self.author.group, "P3121")

    def test_name_setter_valid(self):
        """
        Тест корректного изменения имени через сеттер.
        """
        # Устанавливаем новое имя
        self.author.name = "Имя2"
        # Проверяем, что имя изменилось
        self.assertEqual(self.author.name, "Имя2")

    def test_name_setter_invalid_type(self):
        """
        Тест некорректного типа данных при изменении имени.\
        """
        with self.assertRaises(ValueError):
            self.author.name = 123

    def test_name_setter_short_name(self):
        """
        Тест слишком короткого имени.
        """
        # Пытаемся установить имя из одного символа
        with self.assertRaises(ValueError):
            self.author.name = "А"

    def test_group_setter_valid(self):
        """
        Тест корректного изменения группы.
        """
        self.author.group = "P3122"
        self.assertEqual(self.author.group, "P3122")

    def test_group_setter_invalid_type(self):
        """
        Тест некорректного типа данных при изменении группы.
        """
        with self.assertRaises(ValueError):
            self.author.group = 12345

    def test_group_setter_short_group(self):
        """
        Тест слишком короткой группы.
        """
        with self.assertRaises(ValueError):
            self.author.group = "123"  # Длина 3 < 5


class TestApp(unittest.TestCase):
    """
    Тестирование класса App (Приложение).
    """

    def setUp(self):
        """
        Метод, выполняемый перед каждым тестом.
        """
        # Создаем автора с группой длиной 6 символов
        self.author = Author("Автор", "P31211", 'http/.../')
        # Создаем приложение с тестовыми данными
        self.app = App("Тестовое приложение", "1.0", self.author)

    def test_initialization(self):
        """
        Тест инициализации объекта App.
        """
        self.assertEqual(self.app.name, "Тестовое приложение")
        self.assertEqual(self.app.version, "1.0")
        self.assertEqual(self.app.author, self.author)

    def test_name_setter_valid(self):
        """
        Тест корректного изменения названия приложения.
        """
        self.app.name = "Новое название"
        self.assertEqual(self.app.name, "Новое название")

    def test_name_setter_invalid_empty(self):
        """
        Тест пустого названия приложения.
        """
        with self.assertRaises(ValueError):
            self.app.name = ""

    def test_name_setter_invalid_type(self):
        """
        Тест некорректного типа данных для названия.
        """
        with self.assertRaises(ValueError):
            self.app.name = 123

    def test_version_setter_valid(self):
        """
        Тест корректного изменения версии приложения.
        """

        self.app.version = "2.0"
        self.assertEqual(self.app.version, "2.0")


    def test_author_setter_valid(self):
        """
        Тест корректного изменения автора приложения.
        """
        new_author = Author("Другой Автор", "P31222", 'http:/..../')

        self.app.author = new_author
        self.assertEqual(self.app.author, new_author)

    def test_author_setter_invalid(self):
        """
        Тест некорректного типа данных для автора.
        """
        # Пытаемся установить автора как строку
        with self.assertRaises(TypeError):
            self.app.author = "Не автор"


class TestCurrency(unittest.TestCase):
    """
    Тестирование класса Currency (Валюта).
    """

    def setUp(self):
        """
        Метод, выполняемый перед каждым тестом.
        Создает экземпляр Currency с тестовыми данными.
        """
        # Создаем валюту USD с тестовыми данными
        self.currency = Currency(1, 840, "USD", "Доллар США", 75.50, 1)

    def test_initialization(self):
        """
        Тест инициализации объекта Currency.
        """
        # Проверяем все свойства валюты
        self.assertEqual(self.currency.id, 1)
        self.assertEqual(self.currency.num_code, 840)
        self.assertEqual(self.currency.name_v, "USD")
        self.assertEqual(self.currency.char_code, "Доллар США")
        self.assertEqual(self.currency.value, 75.50)
        self.assertEqual(self.currency.nominal, 1)

    def test_id_setter_invalid_negative(self):
        """
        Тест отрицательного ID валюты.
        """
        # Пытаемся установить отрицательный ID
        with self.assertRaises(ValueError):
            self.currency.id = -1

    def test_num_code_setter_valid(self):
        """
        Тест корректного изменения цифрового кода валюты.
        """

        self.currency.num_code = 978
        self.assertEqual(self.currency.num_code, 978)

    def test_num_code_setter_invalid_range(self):
        """
        Тест некорректного диапазона цифрового кода.
        """
        with self.assertRaises(ValueError):
            self.currency.num_code = 0
        with self.assertRaises(ValueError):
            self.currency.num_code = 1000

    def test_char_code_setter_valid(self):
        """
        Тест корректного изменения символьного кода валюты.
        """
        self.currency.char_code = "EUR"
        self.assertEqual(self.currency.char_code, "EUR")

    def test_char_code_setter_invalid_length(self):
        """
        Тест некорректной длины символьного кода.
        """
        with self.assertRaises(ValueError):
            self.currency.char_code = "US"
        with self.assertRaises(ValueError):
            self.currency.char_code = "USDX"

    def test_value_setter_valid(self):
        """
        Тест корректного изменения курса валюты.
        """
        self.currency.value = 80.25
        self.assertEqual(self.currency.value, 80.25)

    def test_value_setter_invalid_type(self):
        """
        Тест некорректного типа данных для курса валюты.
        """
        with self.assertRaises(ValueError):
            self.currency.value = "не число"

    def test_nominal_setter_valid(self):
        """
        Тест корректного изменения номинала валюты.
        """
        self.currency.nominal = 100
        self.assertEqual(self.currency.nominal, 100)

    def test_nominal_setter_invalid(self):
        """
        Тест некорректных значений номинала.
        """
        with self.assertRaises(ValueError):
            self.currency.nominal = 0
        with self.assertRaises(ValueError):
            self.currency.nominal = -10


class TestUser(unittest.TestCase):
    """
    Тестирование класса User (Пользователь).
    """

    def setUp(self):
        """
        Метод, выполняемый перед каждым тестом.
        """
        # Создаем пользователя с тестовыми данными
        self.user = User("Иван Иванов", 'sfdaohiu@dlfkf', 1)

    def test_initialization(self):
        """
        Тест инициализации объекта User.
        """
        self.assertEqual(self.user.id, 1)
        self.assertEqual(self.user.name, "Иван Иванов")
        self.assertEqual(self.user.mail , 'sfdaohiu@dlfkf')

    def test_id_setter_valid(self):
        """
        Тест корректного изменения ID пользователя.
        """
        self.user.id = 5
        self.assertEqual(self.user.id, 5)

    def test_id_setter_invalid_negative(self):
        """
        Тест отрицательного ID пользователя.
        """
        with self.assertRaises(ValueError):
            self.user.id = -1



class TestUserCurrency(unittest.TestCase):
    """
    Тестирование класса UserCurrency (Связь пользователь-валюта).
    Проверяет корректность работы связи между пользователями и валютами.
    """

    def setUp(self):
        """
        Метод, выполняемый перед каждым тестом.
        """
        self.user_currency = UserCurrency(1, 1, 1)

    def test_initialization(self):
        """
        Тест инициализации объекта UserCurrency.
        """

        self.assertEqual(self.user_currency.id, 1)

        self.assertEqual(self.user_currency.uid, 1)

        self.assertEqual(self.user_currency.current_id, 1)

    def test_all_setters_valid(self):
        """
        Тест корректного изменения всех свойств связи.
        """
        self.user_currency.id = 2
        self.user_currency.uid = 3
        self.user_currency.current_id = 4

        # Проверяем, что все ID изменились
        self.assertEqual(self.user_currency.id, 2)
        self.assertEqual(self.user_currency.uid, 3)
        self.assertEqual(self.user_currency.current_id, 4)

    def test_setters_invalid_negative(self):
        """
        Тест отрицательных значений для всех ID.
        """
        with self.assertRaises(ValueError):
            self.user_currency.id = -1
        with self.assertRaises(ValueError):
            self.user_currency.uid = -1
        with self.assertRaises(ValueError):
            self.user_currency.current_id= -1


if __name__ == '__main__':
    unittest.main()
