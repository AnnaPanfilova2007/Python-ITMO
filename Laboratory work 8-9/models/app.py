from models.author import Author


class App:
    """
    Класс, представляющий приложение с названием, версией и автором.

    Атрибуты:
        __name (str): Название приложения (приватное, без сеттера)
        __version (str): Версия приложения в формате X.X.X
        __author (Author): Объект автора приложения
    """

    def __init__(self, name: str, version: str, author: Author):
        """
        Конструктор класса App.

        Args:
            name (str): Название приложения
            version (str): Версия приложения (должна содержать только цифры и точки)
            author (Author): Объект класса Author - автор приложения

        Инициализирует приватные атрибуты приложения.
        """
        self.__name: str = name  # Приватный атрибут: название приложения
        self.__version: str = version  # Приватный атрибут: версия приложения
        self.__author: Author = author  # Приватный атрибут: автор приложения

    @property
    def version(self):
        """
        Геттер для получения версии приложения.

        Returns:
            str: Текущая версия приложения

        Позволяет получить значение приватного атрибута __version
        """
        return self.__version

    @version.setter
    def version(self, vers: str):
        """
        Сеттер для установки версии приложения с валидацией.

        Args:
            vers (str): Новая версия приложения

        Raises:
            ValueError: Если версия содержит недопустимые символы
                (разрешены только цифры и точки)

        Примеры:
            Допустимо: "1.0", "2.5.3", "10.0.1.5"
            Не допустимо: "1.a", "version-2", "3,5"
        """
        # Проверяем, что все символы в строке - цифры или точки
        if all(s.isdigit() or s == "." for s in vers):
            self.__version = vers
        else:
            raise ValueError("Ошибка при задании версии: разрешены только цифры и точки")

    @property
    def author(self):
        """
        Геттер для получения автора приложения.

        Returns:
            Author: Объект класса Author - автор приложения
        """
        return self.__author

    @author.setter
    def author(self, author: Author):
        """
        Сеттер для установки автора приложения с проверкой типа.

        Args:
            author (Author): Новый автор приложения

        Raises:
            TypeError: Если переданный объект не является экземпляром класса Author

        Обеспечивает строгую типизацию - автор должен быть объектом класса Author
        """
        if isinstance(author, Author):
            self.__author = author
        else:
            raise TypeError("Ошибка при задании класса Автор: ожидается объект класса Author")

    @property
    def name(self):
        """
        Геттер для получения имени автора.

        Returns:
            str: Текущее имя автора

        Позволяет получить значение приватного атрибута __name
        """
        return self.__name

    @name.setter
    def name(self, name: str):
        """
        Сеттер для установки имени автора с валидацией.

        Args:
            name (str): Новое имя автора

        Raises:
            ValueError: Если имя не является строкой или короче 2 символов

        Проверки:
            1. Тип данных должен быть str (используется type(name) is str)
            2. Длина имени должна быть не менее 2 символов
        """
        # Проверка типа через type() is str (строгая проверка типа)
        # Альтернатива: isinstance(name, str) - более гибкая проверка
        if type(name) is str and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError('Ошибка при задании имени автора: имя должно быть строкой длиной не менее 2 символов')
