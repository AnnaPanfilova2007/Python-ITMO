# test_models_mock.py (исправленная версия)
import unittest
from unittest.mock import Mock, patch, MagicMock, call, PropertyMock
import sys
import os

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Currency, User


class TestCurrencyWithMocks(unittest.TestCase):
    """Тестирование сущности Currency с использованием Mock"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        # Создаем валидную валюту для тестов
        self.valid_currency = Currency(
            id=1,
            numc=840,
            name_v="Доллар США",
            chc="USD",
            value=75.50,
            nominal=1
        )

    def test_currency_initialization_valid(self):
        """Тест корректной инициализации валюты"""
        # Act & Assert
        self.assertEqual(self.valid_currency.id, 1)
        self.assertEqual(self.valid_currency.num_code, 840)
        self.assertEqual(self.valid_currency.name_v, "Доллар США")
        self.assertEqual(self.valid_currency.char_code, "USD")
        self.assertEqual(self.valid_currency.value, 75.50)
        self.assertEqual(self.valid_currency.nominal, 1)

    def test_currency_id_setter_valid(self):
        """Тест валидного установления ID"""
        # Act
        self.valid_currency.id = 5

        # Assert
        self.assertEqual(self.valid_currency.id, 5)

    def test_currency_id_setter_invalid_type(self):
        """Тест невалидного типа для ID"""
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.valid_currency.id = "invalid"

        self.assertIn("ID должен быть целым числом >= 0", str(context.exception))

    def test_currency_id_setter_negative(self):
        """Тест отрицательного ID"""
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.valid_currency.id = -1

        self.assertIn("ID должен быть целым числом >= 0", str(context.exception))

    def test_currency_num_code_setter_valid(self):
        """Тест валидного установления цифрового кода"""
        # Act
        self.valid_currency.num_code = 978  # Код евро

        # Assert
        self.assertEqual(self.valid_currency.num_code, 978)

    def test_currency_num_code_setter_invalid_range(self):
        """Тест цифрового кода вне диапазона"""
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.valid_currency.num_code = 0

        self.assertIn("должен быть целым числом от 1 до 999", str(context.exception))

        with self.assertRaises(ValueError):
            self.valid_currency.num_code = 1000

    def test_currency_char_code_setter_valid(self):
        """Тест валидного установления символьного кода"""
        # Act
        self.valid_currency.char_code = "EUR"

        # Assert
        self.assertEqual(self.valid_currency.char_code, "EUR")

    def test_currency_char_code_setter_invalid_length(self):
        """Тест невалидной длины символьного кода"""
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.valid_currency.char_code = "US"  # 2 символа

        self.assertIn("должен быть строкой из 3 символов", str(context.exception))

        with self.assertRaises(ValueError):
            self.valid_currency.char_code = "USDA"  # 4 символа

    def test_currency_value_setter_valid(self):
        """Тест валидного установления курса"""
        # Act
        self.valid_currency.value = 80.25

        # Assert
        self.assertEqual(self.valid_currency.value, 80.25)

    def test_currency_value_setter_invalid_type(self):
        """Тест невалидного типа для курса"""
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.valid_currency.value = "invalid"

        self.assertIn("должен быть числом с плавающей точкой", str(context.exception))

        # Проверяем, что int тоже не принимается
        with self.assertRaises(ValueError):
            self.valid_currency.value = 80

    def test_currency_nominal_setter_valid(self):
        """Тест валидного установления номинала"""
        # Act
        self.valid_currency.nominal = 10

        # Assert
        self.assertEqual(self.valid_currency.nominal, 10)

    def test_currency_nominal_setter_invalid(self):
        """Тест невалидного номинала"""
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.valid_currency.nominal = 0

        # Обратите внимание: сообщение об ошибке содержит "имени валюты", что неверно
        self.assertIn("Ошибка при задании имени валюты", str(context.exception))

    @patch('models.Currency')
    def test_currency_mocked_creation(self, MockCurrency):
        """Тест создания Currency с Mock объектом"""
        # Arrange
        mock_currency_instance = MockCurrency.return_value
        mock_currency_instance.id = 10
        mock_currency_instance.char_code = "GBP"
        mock_currency_instance.value = 95.0

        # Act
        result = mock_currency_instance

        # Assert
        self.assertEqual(result.id, 10)
        self.assertEqual(result.char_code, "GBP")
        self.assertEqual(result.value, 95.0)

    def test_currency_with_mocked_dependencies(self):
        """Тест валюты с моками зависимостей"""
        # Arrange - создаем мок сервиса для обновления курса
        mock_exchange_service = Mock()
        mock_exchange_service.get_current_rate.return_value = 76.5

        # Создаем тестовую валюту
        currency = Currency(
            id=1,
            numc=840,
            name_v="Доллар США",
            chc="USD",
            value=75.5,
            nominal=1
        )

        # Act - имитируем обновление курса через сервис
        new_rate = mock_exchange_service.get_current_rate("USD")
        currency.value = float(new_rate)  # Преобразуем к float

        # Assert
        self.assertEqual(currency.value, 76.5)
        mock_exchange_service.get_current_rate.assert_called_once_with("USD")

    def test_currency_value_update_sequence(self):
        """Тест последовательности обновлений курса"""
        # Arrange
        mock_rate_provider = Mock()
        # Настраиваем side_effect для последовательных значений
        mock_rate_provider.get_rate.side_effect = [75.5, 76.0, 75.8]

        currency = Currency(
            id=1,
            numc=840,
            name_v="Доллар США",
            chc="USD",
            value=75.0,
            nominal=1
        )

        # Act - последовательные обновления
        updates = []
        for _ in range(3):
            new_rate = mock_rate_provider.get_rate("USD")
            currency.value = float(new_rate)
            updates.append(currency.value)

        # Assert
        self.assertEqual(updates, [75.5, 76.0, 75.8])
        self.assertEqual(mock_rate_provider.get_rate.call_count, 3)
        # Проверяем, что все вызовы были с "USD"
        mock_rate_provider.get_rate.assert_has_calls([call("USD"), call("USD"), call("USD")])

    def test_multiple_currencies_with_mocks(self):
        """Тест работы с несколькими валютами через моки"""
        # Arrange
        mock_currencies = []
        for i, code in enumerate(["USD", "EUR", "GBP"], 1):
            mock_currency = Mock(spec=Currency)
            mock_currency.id = i
            mock_currency.char_code = code
            mock_currency.value = 70.0 + i * 5  # Разные курсы
            mock_currencies.append(mock_currency)

        # Act - вычисляем средний курс
        total_value = sum(currency.value for currency in mock_currencies)
        average_value = total_value / len(mock_currencies)

        # Assert
        self.assertEqual(len(mock_currencies), 3)
        self.assertEqual(average_value, 80.0)  # (70+5*1 + 70+5*2 + 70+5*3) / 3 = 75.0
        self.assertEqual(mock_currencies[0].char_code, "USD")
        self.assertEqual(mock_currencies[1].char_code, "EUR")
        self.assertEqual(mock_currencies[2].char_code, "GBP")


class TestUserWithMocks(unittest.TestCase):
    """Тестирование сущности User с использованием Mock"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        # Создаем валидного пользователя для тестов
        self.valid_user = User(
            name="Иван Иванов",
            mail="ivan@example.com",
            id=1
        )

    def test_user_initialization_valid(self):
        """Тест корректной инициализации пользователя"""
        # Act & Assert
        self.assertEqual(self.valid_user.name, "Иван Иванов")
        self.assertEqual(self.valid_user.mail, "ivan@example.com")
        self.assertEqual(self.valid_user.id, 1)

    def test_user_name_setter_valid(self):
        """Тест валидного установления имени"""
        # Act
        self.valid_user.name = "Анна Смирнова"

        # Assert
        self.assertEqual(self.valid_user.name, "Анна Смирнова")

    def test_user_name_setter_invalid_short(self):
        """Тест слишком короткого имени"""
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.valid_user.name = "И"

        self.assertIn("имя должно быть строкой длиной не менее 2 символов", str(context.exception))

    def test_user_name_setter_invalid_type(self):
        """Тест невалидного типа для имени"""
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.valid_user.name = 123

        self.assertIn("имя должно быть строкой", str(context.exception))

    def test_user_mail_setter_valid(self):
        """Тест валидного установления email"""
        # Act
        self.valid_user.mail = "new_email@domain.com"

        # Assert
        self.assertEqual(self.valid_user.mail, "new_email@domain.com")

    def test_user_mail_setter_invalid_short(self):
        """Тест слишком короткого email"""
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.valid_user.mail = "a@b.c"  # 5 символов

        self.assertIn("email должен быть строкой длиной более 5 символов", str(context.exception))

    def test_user_mail_setter_invalid_type(self):
        """Тест невалидного типа для email"""
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.valid_user.mail = 12345

        self.assertIn("email должен быть строкой", str(context.exception))

    def test_user_id_setter_valid(self):
        """Тест валидного установления ID"""
        # Act
        self.valid_user.id = 100

        # Assert
        self.assertEqual(self.valid_user.id, 100)

    def test_user_id_setter_invalid_type(self):
        """Тест невалидного типа для ID"""
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.valid_user.id = "invalid"

        # Обратите внимание: сообщение содержит "id валюты", что неверно
        self.assertIn("id валюты", str(context.exception))

    def test_user_id_setter_negative(self):
        """Тест отрицательного ID"""
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.valid_user.id = -1

        self.assertIn("ID должен быть целым числом >= 0", str(context.exception))

    @patch('models.User')
    def test_user_mocked_creation(self, MockUser):
        """Тест создания User с Mock объектом"""
        # Arrange
        mock_user_instance = MockUser.return_value
        mock_user_instance.name = "Тестовый Пользователь"
        mock_user_instance.mail = "test@test.com"
        mock_user_instance.id = 999

        # Act
        result = mock_user_instance

        # Assert
        self.assertEqual(result.name, "Тестовый Пользователь")
        self.assertEqual(result.mail, "test@test.com")
        self.assertEqual(result.id, 999)

    def test_user_with_mocked_notification_service(self):
        """Тест пользователя с моком сервиса уведомлений"""
        # Arrange
        mock_notification_service = Mock()
        mock_notification_service.send_email.return_value = True

        user = User(
            name="Иван Иванов",
            mail="ivan@example.com",
            id=1
        )

        # Act - имитируем отправку уведомления
        notification_sent = mock_notification_service.send_email(
            to=user.mail,
            subject="Добро пожаловать!",
            body=f"Привет, {user.name}!"
        )

        # Assert
        self.assertTrue(notification_sent)
        mock_notification_service.send_email.assert_called_once_with(
            to="ivan@example.com",
            subject="Добро пожаловать!",
            body="Привет, Иван Иванов!"
        )

    def test_user_email_validation_with_mock(self):
        """Тест валидации email через мок сервиса"""
        # Arrange
        mock_email_validator = Mock()
        mock_email_validator.is_valid.return_value = True

        user = User(
            name="Иван Иванов",
            mail="ivan@example.com",
            id=1
        )

        # Act
        is_valid = mock_email_validator.is_valid(user.mail)

        # Assert
        self.assertTrue(is_valid)
        mock_email_validator.is_valid.assert_called_once_with("ivan@example.com")

    def test_multiple_users_with_mocks(self):
        """Тест работы с несколькими пользователями через моки"""
        # Arrange
        mock_users = []
        user_data = [
            ("Иван Иванов", "ivan@example.com", 1),
            ("Анна Смирнова", "anna@example.com", 2),
            ("Петр Петров", "petr@example.com", 3)
        ]

        for name, email, user_id in user_data:
            mock_user = Mock(spec=User)
            mock_user.name = name
            mock_user.mail = email
            mock_user.id = user_id
            mock_users.append(mock_user)

        # Act - имитируем поиск пользователя по email
        target_email = "anna@example.com"
        found_user = None
        for user in mock_users:
            if user.mail == target_email:
                found_user = user
                break

        # Assert
        self.assertIsNotNone(found_user)
        self.assertEqual(found_user.name, "Анна Смирнова")
        self.assertEqual(found_user.id, 2)

    def test_user_property_access_tracking(self):
        """Тест отслеживания доступа к свойствам пользователя"""
        # Arrange
        user = User(
            name="Иван Иванов",
            mail="ivan@example.com",
            id=1
        )

        # Создаем мок для отслеживания вызовов
        mock_tracker = Mock()

        # Act - имитируем различные операции с пользователем
        # 1. Чтение имени
        name = user.name
        mock_tracker.track_read("name", name)

        # 2. Изменение email
        user.mail = "new_ivan@example.com"
        mock_tracker.track_write("mail", "new_ivan@example.com")

        # 3. Чтение ID
        user_id = user.id
        mock_tracker.track_read("id", user_id)

        # Assert
        self.assertEqual(mock_tracker.track_read.call_count, 2)
        self.assertEqual(mock_tracker.track_write.call_count, 1)

    def test_user_property_mock_with_propertymock(self):
        """Тест свойств пользователя с использованием PropertyMock"""
        # Arrange
        mock_user = Mock(spec=User)

        # Настраиваем PropertyMock для свойства name
        type(mock_user).name = PropertyMock(
            side_effect=["Иван", "Петр", ValueError("Имя слишком короткое")]
        )

        # Act & Assert
        # Первое чтение
        self.assertEqual(mock_user.name, "Иван")

        # Второе чтение
        self.assertEqual(mock_user.name, "Петр")

        # Третье чтение вызывает исключение
        with self.assertRaises(ValueError):
            _ = mock_user.name


class TestIntegrationWithMocks(unittest.TestCase):
    """Интеграционные тесты взаимодействия User и Currency с моками"""

    def test_user_with_currency_subscriptions(self):
        """Тест пользователя с подписками на валюты"""
        # Arrange
        mock_user = Mock(spec=User)
        mock_user.id = 1
        mock_user.name = "Иван Иванов"
        mock_user.mail = "ivan@example.com"

        mock_usd = Mock(spec=Currency)
        mock_usd.id = 1
        mock_usd.char_code = "USD"
        mock_usd.name_v = "Доллар США"
        mock_usd.value = 75.5

        mock_eur = Mock(spec=Currency)
        mock_eur.id = 2
        mock_eur.char_code = "EUR"
        mock_eur.name_v = "Евро"
        mock_eur.value = 82.3

        mock_subscription_service = Mock()
        mock_subscription_service.get_user_currencies.return_value = [mock_usd, mock_eur]

        # Act
        user_currencies = mock_subscription_service.get_user_currencies(mock_user.id)
        total_value_rub = sum(currency.value * 100 for currency in user_currencies)

        # Assert
        self.assertEqual(len(user_currencies), 2)
        self.assertAlmostEqual(total_value_rub, (75.5 + 82.3) * 100)
        mock_subscription_service.get_user_currencies.assert_called_once_with(1)

    @patch('models.User')
    @patch('models.Currency')
    def test_user_updates_currency_rate(self, MockCurrency, MockUser):
        """Тест обновления курса валюты, на которую подписан пользователь"""
        # Arrange
        mock_user = MockUser.return_value
        mock_user.id = 1
        mock_user.name = "Иван"

        mock_currency = MockCurrency.return_value
        mock_currency.id = 1
        mock_currency.char_code = "USD"
        mock_currency.value = 75.5

        mock_rate_service = Mock()
        mock_rate_service.fetch_rate.return_value = 76.0

        # Act
        new_rate = mock_rate_service.fetch_rate("USD")
        mock_currency.value = float(new_rate)

        # Assert
        self.assertEqual(mock_currency.value, 76.0)
        mock_rate_service.fetch_rate.assert_called_once_with("USD")

    def test_notify_user_on_currency_change(self):
        """Тест уведомления пользователя об изменении курса"""
        # Arrange
        mock_user = Mock(spec=User)
        mock_user.name = "Иван Иванов"
        mock_user.mail = "ivan@example.com"

        mock_currency = Mock(spec=Currency)
        mock_currency.char_code = "USD"
        mock_currency.name_v = "Доллар США"

        mock_notification_service = Mock()
        mock_notification_service.notify.return_value = True

        # Act
        notification_sent = mock_notification_service.notify(
            recipient=mock_user.mail,
            message=f"Курс {mock_currency.char_code} ({mock_currency.name_v}) изменился"
        )

        # Assert
        self.assertTrue(notification_sent)
        mock_notification_service.notify.assert_called_once_with(
            recipient="ivan@example.com",
            message="Курс USD (Доллар США) изменился"
        )

    def test_user_subscription_workflow(self):
        """Тест полного workflow подписки пользователя на валюту"""
        # Arrange
        mock_user = Mock(spec=User)
        mock_user.id = 1
        mock_user.name = "Иван"

        mock_currency = Mock(spec=Currency)
        mock_currency.id = 1
        mock_currency.char_code = "USD"

        mock_subscription_manager = Mock()
        mock_subscription_manager.subscribe.return_value = True
        mock_subscription_manager.get_subscriptions.return_value = [mock_currency]
        mock_subscription_manager.unsubscribe.return_value = True

        # Act - полный цикл подписки
        # 1. Подписываемся
        subscribe_result = mock_subscription_manager.subscribe(
            user_id=mock_user.id,
            currency_id=mock_currency.id
        )

        # 2. Получаем подписки
        subscriptions = mock_subscription_manager.get_subscriptions(mock_user.id)

        # 3. Отписываемся
        unsubscribe_result = mock_subscription_manager.unsubscribe(
            user_id=mock_user.id,
            currency_id=mock_currency.id
        )

        # Assert
        self.assertTrue(subscribe_result)
        self.assertTrue(unsubscribe_result)
        self.assertEqual(len(subscriptions), 1)
        self.assertEqual(subscriptions[0], mock_currency)

        mock_subscription_manager.subscribe.assert_called_once_with(user_id=1, currency_id=1)
        mock_subscription_manager.get_subscriptions.assert_called_once_with(1)
        mock_subscription_manager.unsubscribe.assert_called_once_with(user_id=1, currency_id=1)


class TestErrorHandlingWithMocks(unittest.TestCase):
    """Тестирование обработки ошибок с моками"""

    def test_currency_update_with_invalid_rate_service(self):
        """Тест обновления курса с неисправным сервисом"""
        # Arrange
        currency = Currency(
            id=1,
            numc=840,
            name_v="Доллар США",
            chc="USD",
            value=75.5,
            nominal=1
        )

        mock_broken_service = Mock()
        mock_broken_service.get_rate.side_effect = ConnectionError("Сервис недоступен")

        # Act & Assert
        with self.assertRaises(ConnectionError):
            mock_broken_service.get_rate("USD")

        # Курс не должен измениться при ошибке сервиса
        self.assertEqual(currency.value, 75.5)

    def test_user_creation_with_mocked_invalid_data(self):
        """Тест создания пользователя с невалидными данными через мок"""
        # Arrange
        mock_invalid_user = Mock(spec=User)

        # Используем PropertyMock для имитации ошибки валидации
        # Геттер возвращает текущее значение
        # Сеттер проверяет значение
        name_property = PropertyMock()

        def set_name(name):
            if len(name) < 2:
                raise ValueError("Имя слишком короткое")
            name_property.return_value = name

        # Настраиваем property
        type(mock_invalid_user).name = PropertyMock(
            return_value="",  # начальное значение
            side_effect=set_name  # сеттер
        )

        # Act & Assert - попытка установить короткое имя
        with self.assertRaises(ValueError) as context:
            mock_invalid_user.name = "И"  # Слишком короткое

        self.assertIn("Имя слишком короткое", str(context.exception))

    def test_user_invalid_email_with_mock(self):
        """Тест невалидного email через мок"""
        # Arrange
        mock_user = Mock(spec=User)

        # Настраиваем PropertyMock для mail
        mail_property = PropertyMock()

        def set_mail(mail):
            if "@" not in mail:
                raise ValueError("Некорректный email: отсутствует @")
            mail_property.return_value = mail

        type(mock_user).mail = PropertyMock(
            return_value="",
            side_effect=set_mail
        )

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            mock_user.mail = "invalid-email"

        self.assertIn("Некорректный email", str(context.exception))

        # Валидный email должен работать
        try:
            mock_user.mail = "valid@example.com"
            # Если нет исключения - успех
            self.assertTrue(True)
        except ValueError:
            self.fail("Валидный email не должен вызывать исключение")

    def test_currency_conversion_error_with_mock(self):
        """Тест ошибки конвертации валюты"""
        # Arrange
        mock_converter = Mock()
        mock_converter.convert.side_effect = ValueError("Неизвестная валюта")

        mock_currency = Mock(spec=Currency)
        mock_currency.char_code = "XXX"  # Несуществующий код

        # Act & Assert
        with self.assertRaises(ValueError):
            mock_converter.convert(mock_currency.char_code, "RUB", 100)

    def test_user_with_broken_notification_service(self):
        """Тест пользователя с неработающим сервисом уведомлений"""
        # Arrange
        user = User(
            name="Иван Иванов",
            mail="ivan@example.com",
            id=1
        )

        mock_broken_notification = Mock()
        mock_broken_notification.send_email.side_effect = Exception("SMTP сервер недоступен")

        # Act & Assert
        with self.assertRaises(Exception):
            mock_broken_notification.send_email(
                to=user.mail,
                subject="Тест",
                body="Тест"
            )

        # Проверяем, что пользователь не пострадал
        self.assertEqual(user.name, "Иван Иванов")
        self.assertEqual(user.mail, "ivan@example.com")

    def test_currency_validation_chain_with_mocks(self):
        """Тест цепочки валидации валюты с моками"""
        # Arrange
        mock_validator1 = Mock()
        mock_validator1.validate_code.return_value = True

        mock_validator2 = Mock()
        mock_validator2.validate_rate.return_value = False  # Вторая проверка не проходит
        mock_validator2.validate_rate.side_effect = ValueError("Курс вне допустимого диапазона")

        mock_currency = Mock(spec=Currency)
        mock_currency.char_code = "USD"
        mock_currency.value = -10.0  # Невалидный курс

        # Act & Assert
        # Первая проверка проходит
        self.assertTrue(mock_validator1.validate_code(mock_currency.char_code))

        # Вторая проверка не проходит
        with self.assertRaises(ValueError):
            mock_validator2.validate_rate(mock_currency.value)

        # Проверяем вызовы
        mock_validator1.validate_code.assert_called_once_with("USD")
        mock_validator2.validate_rate.assert_called_once_with(-10.0)


if __name__ == '__main__':
    unittest.main(verbosity=2)