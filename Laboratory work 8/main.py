from jinja2 import Environment, PackageLoader, select_autoescape
from models import Author, User
from controllers import databasecontroller
from controllers import CurrencyRatesCRUD
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from utilits import currencies_api


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
        m_autor = Author('Anna Panfilova', 'P3121')
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
            User("Иван Иванов", "ivan@example.com", "1"),
            User("Анна Смирнова", "anna.s@mail.ru", "2"),
            User("Петр Петров", "petrov.p@yandex.ru", "3"),
            User("Мария Сидорова", "maria.sidorova@gmail.com", "4"),
            User("Алексей Козлов", "alex.kozlov@yandex.ru", "5"),
            User("Ольга Новикова", "olga.novikova@mail.com", "6")
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
        # Обработка отдельного пользователя по ID
        pass

    def handle_currencies_list(self):
        ...


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
