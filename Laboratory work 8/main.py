from jinja2 import Environment, PackageLoader, select_autoescape
import models
from controllers import databasecontroller
from controllers import CurrencyRatesCRUD
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from utilits.currencies_api import get_currencies
from datetime import datetime

currencies = [
    "USD",  # Доллар США (United States Dollar)
    "EUR",  # Евро (Euro)
    "JPY",  # Японская иена (Japanese Yen)
    "GBP",  # Фунт стерлингов (British Pound)
    "CHF",  # Швейцарский франк (Swiss Franc)
    "CAD",  # Канадский доллар (Canadian Dollar)
    "AUD",  # Австралийский доллар (Australian Dollar)
    "CNY",  # Китайский юань (Chinese Yuan)
    "NZD",  # Новозеландский доллар (New Zealand Dollar)
    "INR"   # Индийская рупия (Indian Rupee)
]

currenci_dict = get_currencies(currencies, url="https://www.cbr-xml-daily.ru/daily_json.js")

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)

        if path == '/':
            self.handle_main_page()
        elif path == '/users':
            self.handle_users_list()
        elif path == '/user':
            self.handle_user(query_params)
        elif path == '/currencies':
            self.handle_currencies_list()
        elif path == '/author':
            self.handle_author_info()
        else:
            self.send_error(404, "Страница не найдена")

    def handle_main_page(self):
        m_autor = models.Author('Anna Panfilova', 'P3121')
        template = env.get_template("main.html")
        result = template.render(
            navigation=[
                # Каждая кнопка - отдельный элемент массива
                {
                    'caption': 'Больше об авторе',
                    'href': "http://localhost:8080/Author"
                },
                {
                    'caption': 'Пользователи',
                    'href': "http://localhost:8080/users"
                },
                {
                    'caption': 'Список Валют',
                    'href': "http://localhost:8080/currencies"
                }
            ],
            author_name=m_autor.name,
            group=m_autor.group)
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(result.encode('utf-8'))

    def handle_users_list(self):
        # Создаем список пользователей
        users = [
            models.User("Иван Иванов", "ivan@example.com", 1),
            models.User("Анна Смирнова", "anna.s@mail.ru", 2),
            models.User("Петр Петров", "petrov.p@yandex.ru", 3),
            models.User("Мария Сидорова", "maria.sidorova@gmail.com", 4),
            models.User("Алексей Козлов", "alex.kozlov@yandex.ru", 5),
            models.User("Ольга Новикова", "olga.novikova@mail.com", 6)
        ]

        template = env.get_template("users.html")
        res = template.render(
            users=users,  # Передаем весь список пользователей
            total_users=len(users)
        )
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(res.encode('utf-8'))

    def handle_user(self, query_params):
        users = [
            models.User("Иван Иванов", "ivan@example.com", 1),
            models.User("Анна Смирнова", "anna.s@mail.ru", 2),
            models.User("Петр Петров", "petrov.p@yandex.ru", 3),
            models.User("Мария Сидорова", "maria.sidorova@gmail.com", 4),
            models.User("Алексей Козлов", "alex.kozlov@yandex.ru", 5),
            models.User("Ольга Новикова", "olga.novikova@mail.com", 6)
        ]
        user_currencies_list = [
            models.UserCurrency(1, 1, 1),
            models.UserCurrency(2, 1, 4),
            models.UserCurrency(3, 2, 6),
            models.UserCurrency(4, 2, 9),
            models.UserCurrency(5, 3, 7),
            models.UserCurrency(6, 1, 6),
            models.UserCurrency(7, 4, 8),
            models.UserCurrency(8, 2, 5),
            models.UserCurrency(9, 6, 6),
            models.UserCurrency(10, 2, 1),
            models.UserCurrency(11, 5, 4),
            models.UserCurrency(12, 3, 2),
            models.UserCurrency(13, 5, 4),
            models.UserCurrency(14, 1, 7),
            models.UserCurrency(15, 3, 9),
            models.UserCurrency(16, 4, 1),
            models.UserCurrency(17, 2, 5),
            models.UserCurrency(18, 6, 3),
            models.UserCurrency(19, 4, 5),
            models.UserCurrency(20, 2, 3),
            models.UserCurrency(21, 6, 6),
            models.UserCurrency(22, 5, 8)
        ]


    def handle_currencies_list(self):
        currenci_list = [
            models.Currency(1, 840, "Доллар США", "USD", currenci_dict.get("USD", 0), 1),
            models.Currency(2, 978, "Евро", "EUR", currenci_dict.get("EUR", 0), 1),
            models.Currency(3, 392, "Японская иена", "JPY", currenci_dict.get("JPY", 0), 1),
            models.Currency(4, 826, "Фунт стерлингов", "GBP", currenci_dict.get("GBP", 0), 1),
            models.Currency(5, 756, "Швейцарский франк", "CHF", currenci_dict.get("CHF", 0), 1),
            models.Currency(6, 124, "Канадский доллар", "CAD", currenci_dict.get("CAD", 0), 1),
            models.Currency(7, 36, "Австралийский доллар", "AUD", currenci_dict.get("AUD", 0), 1),
            models.Currency(8, 156, "Китайский юань", "CNY", currenci_dict.get("CNY", 0), 1),
            models.Currency(9, 554, "Новозеландский доллар", "NZD", currenci_dict.get("NZD", 0), 1),
            models.Currency(10, 356, "Индийская рупия", "INR", currenci_dict.get("INR", 0), 1)
        ]

        template = env.get_template("currencies.html")
        res = template.render(
            currencies=currenci_list,
            total_currencies=len(currenci_list),
            now=datetime.now().strftime("%d.%m.%Y %H:%M")  # Добавляем текущее время
        )
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(res.encode('utf-8'))



    def handle_author_info(self):
        # Обработка информации об авторе
        pass


env = Environment(
    loader=PackageLoader("main"),
    autoescape=select_autoescape()
)

if __name__ == '__main__':
    print('server is running')
    httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
    httpd.serve_forever()
