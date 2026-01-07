import urllib

from jinja2 import Environment, PackageLoader, select_autoescape
import models
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from utilits.currencies_api import get_currencies
from datetime import datetime
from controllers import CurrencyRatesCRUD, CurrencyController, PagesController
from typing import Dict, List, Any, Optional

db_controller = CurrencyRatesCRUD(None)  # Контроллер для работы с базой данных валют
currency_controller = CurrencyController(db_controller)  # Контроллер бизнес-логики валют
pages_controller = PagesController()  # Контроллер для рендеринга HTML-страниц
db_controller._create()  # Создание необходимых таблиц в базе данных



class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Разделяем путь и параметры запроса, парсим параметры в словарь
        url_query_dict: Dict[str, List[str]] = parse_qs(self.path.rpartition('?')[-1])
        path: str = self.path.split('?')[0]
        result: str = ""

        m_autor = models.Author('Anna Panfilova', 'P3121', "https://github.com/AnnaPanfilova2007/Python-ITMO/tree/main/Laboratory%20work%208")
        m_app = models.App("Приложение для\nотслеживания\nкурса валют", "1.0", m_autor)
        global m_autor, m_app, url_query_dict
        if path == '/':
            self.handle_main_page(str)
        elif path == '/users':
            self.handle_users_list(str)
        elif path == '/user':
            self.handle_user(str, query_params)
        elif path == '/currencies':
            self.handle_currencies_list(str)
        elif path == '/author':
            self.handle_author_info(str)
        else:
            self.send_error(404, "Страница не найдена")

    def handle_main_page(self, str: str):
        template = env.get_template("main.html")
        currencies: List[Dict[str, Any]] = currency_controller.list_currencies()
        result = pages_controller.render_index(
            currencies,
            m_autor.name,
            m_autor.group,
            m_app.name,
            m_app.version
        )
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(result.encode('utf-8'))

    def handle_users_list(self, base_data):
        template = env.get_template("users.html")
        # Получаем список пользователей из контроллера
        users: List[Dict[str, Any]] = currency_controller.get_users()
        # Рендерим страницу пользователей
        result = pages_controller.render_users(m_app.name, users)
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(result.encode('utf-8'))

    def handle_user(self, base_data, query_params):
        if 'id' in query_params:
            try:
                user_id: int = int(url_query_dict['id'][0])
                # Получаем данные пользователя по ID
                user: Optional[Dict[str, Any]] = currency_controller.get_user(user_id)

                if user:
                    user_currencies: List[Dict[str, Any]] = currency_controller.get_user_currencies(user_id)
                    # Рендерим страницу пользователя
                    result = pages_controller.render_user(m_app.name, user, user_currencies)

                    # Рендеринг страницы пользователя
                    template_user = env.get_template("user_detail.html")
                    result = template_user.render(**base_data)

                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(result.encode('utf-8'))
                    return
                else:
                    # Пользователь не найден
                    self.send_error(404, "Пользователь не найден")
                    return

            except ValueError:
                self.send_error(400, "Некорректный идентификатор пользователя")
                return
        else:
            self.send_error(400, "Не указан параметр id")
            return

    def handle_currencies_list(self, base_data):
        template = env.get_template("currencies.html")
        base_data['currencies'] = currenci_list
        base_data['total_currencies'] = len(currenci_list)
        base_data['now'] = datetime.now().strftime("%d.%m.%Y %H:%M")
        result = template.render(**base_data)
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(result.encode('utf-8'))

    def handle_author_info(self, base_data):
        template = env.get_template("author.html")
        result = template.render(**base_data)
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(result.encode('utf-8'))

env = Environment(
    loader=PackageLoader("main"),
    autoescape=select_autoescape()
)

if __name__ == '__main__':
    print('server is running')
    httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
    httpd.serve_forever()