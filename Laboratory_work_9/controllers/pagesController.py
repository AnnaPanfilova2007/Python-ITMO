from jinja2 import Environment, PackageLoader, select_autoescape
from typing import List, Dict, Any


class PagesController:
    """
    Контроллер для рендеринга HTML-страниц приложения.
    """

    def __init__(self) -> None:
        """
        Инициализирует окружение Jinja2 для работы с шаблонами.

        """
        # Инициализация окружения Jinja2 с загрузчиком шаблонов
        self.env: Environment = Environment(
            loader=PackageLoader("main"),  # Загрузчик шаблонов из пакета "myapp"
            autoescape=select_autoescape()  # Автоматическое экранирование HTML
        )

    def render_index(self, currencies: List[Dict[str, Any]], author_name: str,
                     group: str, app_name: str, version: str) -> str:
        """
        Рендерит главную страницу приложения.

        Аргументы:
            currencies: Список валют для отображения
            author_name: Имя автора приложения
            group: Группа автора
            app_name: Название приложения
            version: Версия приложения

        Возвращает:
            str: HTML-код главной страницы
        """
        # Загрузка шаблона index.html
        template = self.env.get_template("main.html")
        # Рендеринг шаблона с передачей данных и навигации
        return template.render(
            currencies=currencies,  # Список валют
            author_name=author_name,  # Имя автора
            group=group,  # Группа автора
            app_name=app_name,  # Название приложения
            version=version,  # Версия приложения
            # Навигационное меню для главной страницы
            navigation=[
                {'caption': 'Главная', 'href': '/'},
                {'caption': 'Пользователи', 'href': '/users'},
                {'caption': 'Валюты', 'href': '/currencies'},
                {'caption': 'Об авторе', 'href': '/author'}
            ]
        )

    def render_currencies(self, app_name: str, currencies: List[Dict[str, Any]],
                          result: str = "") -> str:
        """
        Рендерит страницу управления валютами.

        Аргументы:
            app_name: Название приложения
            currencies: Список валют для отображения
            result: Сообщение о результате операции (обновление, удаление и т.д.)

        Возвращает:
            str: HTML-код страницы валют
        """
        # Загрузка шаблона currencies.html
        template = self.env.get_template("currencies.html")
        # Рендеринг шаблона с передачей данных и навигации
        return template.render(
            currencies=currencies,  # Список валют
            result=result,  # Результат операций с валютами
            app_name=app_name,  # Название приложения
            # Навигационное меню для страницы валют
            navigation=[
                {'caption': 'Главная', 'href': '/'},
                {'caption': 'Пользователи', 'href': '/users'},
                {'caption': 'Валюты', 'href': '/currencies'},
                {'caption': 'Об авторе', 'href': '/author'}
            ]
        )

    def render_author(self, author_name: str, group: str,
                      app_name: str, version: str) -> str:
        """
        Рендерит страницу "Об авторе".

        Аргументы:
            author_name: Имя автора приложения
            group: Группа автора
            app_name: Название приложения
            version: Версия приложения

        Возвращает:
            str: HTML-код страницы об авторе
        """
        # Загрузка шаблона author.html
        template = self.env.get_template("Author.html")
        # Рендеринг шаблона с передачей данных и навигации
        return template.render(
            author_name=author_name,  # Имя автора
            group=group,  # Группа автора
            app_name=app_name,  # Название приложения
            version=version,  # Версия приложения
            # Навигационное меню для страницы об авторе
            navigation=[
                {'caption': 'Главная', 'href': '/'},
                {'caption': 'Пользователи', 'href': '/users'},
                {'caption': 'Валюты', 'href': '/currencies'},
                {'caption': 'Об авторе', 'href': '/author'}
            ]
        )

    def render_users(self, app_name: str, users: List[Dict[str, Any]]) -> str:
        """
        Рендерит страницу со списком пользователей.

        Аргументы:
            app_name: Название приложения
            users: Список пользователей для отображения

        Возвращает:
            str: HTML-код страницы пользователей
        """
        # Загрузка шаблона users.html
        template = self.env.get_template("users.html")
        # Рендеринг шаблона с передачей данных и навигации
        return template.render(
            users=users,  # Список пользователей
            app_name=app_name,  # Название приложения
            # Навигационное меню для страницы пользователей
            navigation=[
                {'caption': 'Главная', 'href': '/'},
                {'caption': 'Пользователи', 'href': '/users'},
                {'caption': 'Валюты', 'href': '/currencies'},
                {'caption': 'Об авторе', 'href': '/author'}
            ]
        )

    def render_user(self, app_name: str, user: Dict[str, Any],
                    user_currencies: List[Dict[str, Any]]) -> str:
        """
        Рендерит страницу конкретного пользователя.

        Аргументы:
            app_name: Название приложения
            user: Данные пользователя
            user_currencies: Список валют пользователя

        Возвращает:
            str: HTML-код страницы пользователя
        """
        # Загрузка шаблона user.html
        template = self.env.get_template("user_detail.html")
        # Рендеринг шаблона с передачей данных и навигации
        return template.render(
            user=user,  # Данные пользователя
            user_currencies=user_currencies,  # Валюты пользователя
            app_name=app_name,  # Название приложения
            # Навигационное меню для страницы пользователя
            navigation=[
                {'caption': 'Главная', 'href': '/'},
                {'caption': 'Пользователи', 'href': '/users'},
                {'caption': 'Валюты', 'href': '/currencies'},
                {'caption': 'Об авторе', 'href': '/author'}
            ]
        )