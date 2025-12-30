class CurrencyRatesCRUD():
    def __init__(self, currency_rates_obj):
        import sqlite3
        self.__con = sqlite3.connect(":memory:")
        self.__createtable()
        self.__cursor = self.__con.cursor()
        self.__currency_rates_obj = currency_rates_obj

    def __createtable(self):
        self.__con.execute(
            "CREATE TABLE IF NOT EXISTS currency("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "cur TEXT,"
            "date TEXT,"
            "value FLOAT);")
        self.__con.commit()

    def _create(self):
        __params = self.__currency_rates_obj.values
        # [("USD", "02-04-2025 11:10", "90"), ("EUR", "02-04-2025 11:11", "91")]
        __sqlquery = "INSERT INTO currency(cur, date, value) VALUES(?, ?, ?)"

        # TODO: реализовать именованный стиль запроса
        # This is the named style used with executemany():
        # data = (
        #     {"name": "C", "year": 1972},
        #     {"name": "Fortran", "year": 1957},
        #     {"name": "Python", "year": 1991},
        #     {"name": "Go", "year": 2009},
        # )
        # cur.executemany("INSERT INTO lang VALUES(:name, :year)", data)

        self.__cursor.executemany(__sqlquery, __params)
        self.__con.commit()

    def _read(self):
        # TODO: Реализовать параметризованный запрос на получение значения валют по коду: строка из трех символов
        print('+')
        cur = self.__con.execute("SELECT * FROM currency")
        for _row in cur:
            print(_row)

    def _update(self):
        pass
        # SQL: UPDATE
        # вызвать метод Deprecated

    def _delete(self):
        pass
        # SQL: DELETE


# TODO: данный файл положить в каталог controllers, таким образом создав пакет
# каталог controllers положить в той же папке, что и app.py
# контроллер для отображения данных валют