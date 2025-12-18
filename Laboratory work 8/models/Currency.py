from enum import EnumCheck


class Currency:
    def __init__(self, id: str, numc: str, name_v: str, chc: str, value: str, nominal: str):
        self.__id: str = id
        self.__num_code: str = numc
        self.__name_v: str = name_v
        self.__char_code: str = chc
        self.__value: str = value
        self.__nominal: str = nominal
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id:str):
        try:
            id = int(id)
            self.__id = id
        except:
            raise ValueError("Ошибка при задании id")

    @property
    def num_code(self):
        return self.__num_code

    @num_code.setter
    def num_code(self, numc:str):
        try:
            numc = int(numc)
            self.__num_code = numc
        except:
            raise ValueError("Ошибка при задании цифрового кода")

    @property
    def char_code(self):
        return self.__char_code

    @char_code.setter
    def char_code(self, chc: str):
        if len(chc) == 3 and chc.isalpha():
            self.__char_code = chc
        else:
            raise ValueError("Ошибка при задании кода валюты")

    @property
    def name_v(self):
        return self.__name_v

    @name_v.setter
    def name_v(self, name: str):
        if type(name) is str and len(name) >= 2:
            self.__name_v = name
        else:
            raise ValueError('Ошибка при задании имени автора')

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        try:
            value = float(value)
            self.__value = value
        except:
            raise ValueError("Ошибка при задании курса")

    @property
    def nominal(self):
        return self.__nominal

    @nominal.setter
    def nominal(self, nominal: str):
        try:
            nominal = int(nominal)
            self.__nominal = nominal
        except:
            raise ValueError("Ошибка при задании номинала")


