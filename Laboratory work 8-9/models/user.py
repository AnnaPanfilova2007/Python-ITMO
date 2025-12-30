class User:
    """
    Класс, представляющий пользователя системы.

    Атрибуты:
        __name (str): Имя пользователя (приватное)
        __mail (str): Адрес электронной почты (приватное)
        __id (int): Уникальный идентификатор пользователя (приватное)

    """

    def __init__(self, name: str, mail: str, id: int):
        """
        Конструктор класса User.

        Args:
            name (str): Имя пользователя (минимум 2 символа)
            mail (str): Адрес электронной почты (минимум 6 символов)
            id (int): Уникальный идентификатор (целое число >= 0)
        """
        self.__name: str = name  # Приватный: имя пользователя
        self.__mail: str = mail  # Приватный: email пользователя
        self.__id: int = id  # Приватный: уникальный идентификатор


    @property
    def name(self):
        """
        Геттер для получения имени пользователя.

        Returns:
            str: Текущее имя пользователя

        Позволяет безопасно читать приватный атрибут __name
        """
        return self.__name

    @name.setter
    def name(self, name: str):
        """
        Сеттер для установки имени пользователя с валидацией.

        Args:
            name (str): Новое имя пользователя

        Raises:
            ValueError: Если имя не является строкой или короче 2 символов
        """
        if type(name) is str and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError(
                'Ошибка при задании имени пользователя: имя должно быть строкой длиной не менее 2 символов')

    @property
    def mail(self):
        """
        Геттер для получения mail пользователя.

        Returns:
            str: Текущий адрес электронной почты
        """
        return self.__mail

    @mail.setter
    def mail(self, mail: str):
        """
        Сеттер для установки mail пользователя с валидацией.

        Args:
            mail (str): Новый адрес электронной почты

        Raises:
            ValueError: Если email не является строкой или короче 6 символов


        """
        if type(mail) is str and len(mail) > 5:
            self.__mail = mail
        else:
            raise ValueError('Ошибка при задании почты для рассылки: email должен быть строкой длиной более 5 символов')

    @property
    def id(self):
        """
        Геттер для получения идентификатора пользователя.

        Returns:
            int: Уникальный идентификатор пользователя
        """
        return self.__id

    @id.setter
    def id(self, id: int):
        """
        Сеттер для установки идентификатора пользователя с валидацией.

        Args:
            id (int): Новый идентификатор пользователя

        Raises:
            ValueError: Если ID не является int или меньше 0

        """
        if type(id) is int and id >= 0:
            self.__id = id
        else:
            raise ValueError('Ошибка при задании id валюты: ID должен быть целым числом >= 0')
