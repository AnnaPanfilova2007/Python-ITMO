from Author import Author
class App:
    def __init__(self, name: str, version: str, author: Author):
        self.__name: str = name
        self.__version: str = version
        self.__author: Author = author



    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, vers: str):
        if all(s.isdigit() or s == "." for s in vers):
            self.__version = vers
        else:
            raise ValueError("Ошибка при задании версии")

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, author: str):
        if isinstance(author, Author):
            self.__author = author
        else:
            raise TypeError("Ошибка при задании класса Автор")

