from typing import List, Dict, Optional, Any
from controllers.databasecontroller import CurrencyRatesCRUD


class CurrencyController:
    """Контроллер для операций с валютами."""

    def __init__(self, db_controller: CurrencyRatesCRUD) -> None:
        # Инициализация контроллера с объектом доступа к БД
        self.db = db_controller  # Храним ссылку на контроллер БД

    def list_currencies(self) -> List[Dict[str, Any]]:
        # Получение списка всех валют
        return self.db._read()  # Вызываем метод чтения без параметров

    def update_currency(self, char_code: str, value: float) -> None:
        # Обновление курса валюты по её коду
        self.db._update({char_code: value})  # Передаём словарь с новым значением

    def delete_currency(self, currency_id: int) -> None:
        # Удаление валюты по ID
        self.db._delete(currency_id)  # Передаём ID для удаления

    def get_user_currencies(self, user_id: int) -> List[Dict[str, Any]]:
        # Получение валют конкретного пользователя
        return self.db._read(user_id=user_id)  # Передаём user_id как параметр

    def get_users(self) -> List[Dict[str, Any]]:
        # Получение списка всех пользователей
        return self.db._read(get_users=True)  # Флаг для получения пользователей

    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        # Поиск пользователя по ID
        users = self.db._read(get_users=True)  # Получаем всех пользователей

        for user in users:  # Перебираем пользователей
            if user['id'] == user_id:  # Проверяем совпадение ID
                return user  # Возвращаем найденного пользователя

        return None  # Если не нашли - возвращаем None