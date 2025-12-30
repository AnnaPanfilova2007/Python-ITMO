class Author:
    """
    Класс, представляющий автора с именем и группой.

    Атрибуты:
        __name (str): Имя автора (приватное)
        __group (str): Название группы автора (приватное)

    """

    def __init__(self, name: str, group: str, git: str):
        """
        Конструктор класса Author.

        Args:
            name (str): Имя автора (должно быть строкой длиной >= 2 символов)
            group (str): Группа автора (должна быть строкой длиной > 5 символов)
            git (str): гитхаб автора (должна быть строкой длиной >= 2 символов)

        """
        self.__name: str = name  # Приватный атрибут: имя автора
        self.__group: str = group  # Приватный атрибут: группа автора
        self.__git: str = git #Приватный атрибут: ссылка на гитхаб

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
        Сеттер для установки имени автора

        Args:
            name (str): Новое имя автора

        Raises:
            ValueError: Если имя не является строкой или короче 2 символов

        """
        if type(name) is str and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError('Ошибка при задании имени автора: имя должно быть строкой длиной не менее 2 символов')

    @property
    def group(self):
        """
        Геттер для получения группы автора.

        Returns:
            str: Текущая группа автора
        """
        return self.__group

    @group.setter
    def group(self, group: str):
        """
        Сеттер для установки группы автора с валидацией.

        Args:
            group (str): Новая группа автора

        Raises:
            ValueError: Если группа не является строкой или короче/равна 5 символам


        """
        if type(group) is str and len(group) >= 5:
            self.__group = group
        else:
            raise ValueError('Ошибка при задании группы автора: группа должна быть строкой длиной более 5 символов')

    @property
    def git(self):
        """
        Геттер для получения гитхаба автора.

        Returns:
            str: получает ссылку

        Позволяет получить значение приватного атрибута __git
        """
        return self.__git

    @git.setter
    def git(self, git: str):
        """
        Сеттер для установки ссылки на гит

        Args:
            git (str): Новая ссылка

        Raises:
            ValueError: Если гит не является строкой или короче 2 символов

        """
        if type(git) is str and len(git) >= 2:
            self.__git = git
        else:
            raise ValueError('Ошибка при задании ссылки на гитхаб')
