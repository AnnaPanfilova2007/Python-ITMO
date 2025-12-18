class User:
    def __init__(self, name: str, mail: str, id:str):
        self.__name: str = name
        self.__mail: str = mail
        self.__id: str = id


    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        if type(name) is str and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError('Ошибка при задании имени пользователя')

    @property
    def mail(self):
        return self.__mail

    @mail.setter
    def mail(self, mail: str):
        if type(mail) is str and len(mail) > 5:
            self.__mail = mail
        else:
            raise ValueError('Ошибка при задании почты для рассылки')

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