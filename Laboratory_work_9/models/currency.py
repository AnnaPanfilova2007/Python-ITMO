# Импорт EnumCheck не используется в коде - возможно, это ошибка или остаток от другого кода
# Если EnumCheck действительно нужен, оставьте импорт, иначе удалите строку
# from enum import EnumCheck  # <-- возможно, лишний импорт

class Currency:
    """
    Класс, представляющий валюту с её характеристиками.

    Соответствует структуре валюты из Центрального банка РФ:
    - ID валюты
    - Цифровой код
    - Название валюты
    - Символьный код (например, USD, EUR)
    - Курс валюты к рублю
    - Номинал (единица валюты)

    Все атрибуты приватные с геттерами и сеттерами для контроля целостности данных.
    """

    def __init__(self, id: int, numc: int, name_v: str, chc: str, value: float, nominal: int):
        """
        Конструктор класса Currency.

        Args:
            id (int): Уникальный идентификатор валюты (>= 0)
            numc (int): Цифровой код валюты (1-999)
            name_v (str): Название валюты (например, "Доллар США")
            chc (str): Символьный код валюты (3 символа, например "USD")
            value (float): Курс валюты к рублю
            nominal (int): Номинал валюты (>= 1)

        """
        self.__id: int = id  # Приватный: ID валюты
        self.__num_code: int = numc  # Приватный: цифровой код (ISO 4217 numeric)
        self.__name_v: str = name_v  # Приватный: название валюты
        self.__char_code: str = chc  # Приватный: символьный код (ISO 4217 alphabetic)
        self.__value: float = value  # Приватный: курс к рублю
        self.__nominal: int = nominal  # Приватный: номинал (обычно 1, 10, 100 и т.д.)

    @property
    def id(self):
        """
        Геттер для получения ID валюты.

        Returns:
            int: Уникальный идентификатор валюты
        """
        return self.__id

    @id.setter
    def id(self, id: int):
        """
        Сеттер для установки ID валюты с валидацией.

        Args:
            id (int): Новый ID валюты

        Raises:
            ValueError: Если ID не является int или меньше 0

        """
        if type(id) is int and id >= 0:
            self.__id = id
        else:
            raise ValueError('Ошибка при задании id валюты: ID должен быть целым числом >= 0')

    @property
    def num_code(self):
        """
        Геттер для получения цифрового кода валюты.

        Returns:
            int: Цифровой код валюты (ISO 4217)
        """
        return self.__num_code

    @num_code.setter
    def num_code(self, numc: int):
        """
        Сеттер для установки цифрового кода валюты с валидацией.

        Args:
            numc (int): Новый цифровой код (1-999)

        Raises:
            ValueError: Если код не int или не в диапазоне 1-999

        """
        if type(numc) is int and 1 <= numc <= 999:
            self.__num_code = numc
        else:
            raise ValueError('Ошибка при задании цифрового кода валюты: должен быть целым числом от 1 до 999')

    @property
    def char_code(self):
        """
        Геттер для получения символьного кода валюты.

        Returns:
            str: 3-символьный код валюты (например, "USD", "EUR")
        """
        return self.__char_code

    @char_code.setter
    def char_code(self, chc: str):
        """
        Сеттер для установки символьного кода валюты с валидацией.

        Args:
            chc (str): Новый символьный код (ровно 3 символа)

        Raises:
            ValueError: Если код не str или не 3 символа

        """
        if type(chc) is str and len(chc) == 3:
            self.__char_code = chc
        else:
            raise ValueError('Ошибка при задании символьного кода валюты: должен быть строкой из 3 символов')

    @property
    def name_v(self):
        """
        Геттер для получения названия валюты.

        Returns:
            str: Название валюты (например, "Доллар США")
        """
        return self.__name_v

    @name_v.setter
    def name_v(self, name: str):
        """
        Сеттер для установки названия валюты с валидацией.

        Args:
            name (str): Новое название валюты

        Raises:
            ValueError: Если название не str

        """
        if type(name) is str and len(name) >= 0:  # len(name) >= 0 всегда True для строк
            self.__name_v = name
        else:
            raise ValueError('Ошибка при задании имени валюты: должно быть строкой')

    @property
    def value(self):
        """
        Геттер для получения курса валюты.

        Returns:
            float: Курс валюты к рублю
        """
        return self.__value

    @value.setter
    def value(self, value: float):
        """
        Сеттер для установки курса валюты с валидацией.

        Args:
            value (float): Новый курс валюты

        Raises:
            ValueError: Если курс не float

        """
        if type(value) is float:  # Строгая проверка типа
            self.__value = value
        else:
            raise ValueError('Ошибка при задании курса валюты: должен быть числом с плавающей точкой')

    @property
    def nominal(self):
        """
        Геттер для получения номинала валюты.

        Returns:
            int: Номинал валюты (количество единиц для указанного курса)
        """
        return self.__nominal

    @nominal.setter
    def nominal(self, nominal: int):
        """
        Сеттер для установки номинала валюты с валидацией.

        Args:
            nominal (int): Новый номинал (>= 1)

        Raises:
            ValueError: Если номинал не int или меньше 1
        """
        if type(nominal) is int and nominal >= 1:
            self.__nominal = nominal
        else:
            # ОШИБКА: Сообщение не соответствует проверяемому атрибуту
            # Должно быть: 'Ошибка при задании номинала валюты'
            raise ValueError('Ошибка при задании имени валюты')