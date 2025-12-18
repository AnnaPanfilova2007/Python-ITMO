class UserCurrency:
    def __init__(self, ):
        ...

    @property
    def uid(self):
        return self.__uid
    @uid.setter
    def uid(self, uid:str):
        try:
            uid = int(uid)
            self.__uid = uid
        except:
            raise ValueError("Ошибка в User id")

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: str):
        try:
            id = int(id)
            self.__id = id
        except:
            raise ValueError("Ошибка в id")

    @property
    def current_id(self):
        return self.__cid

    @current_id.setter
    def current_id(self, cid: str):
        try:
            cid = int(cid)
            self.__cid = cid
        except:
            raise ValueError("Ошибка в cid")


