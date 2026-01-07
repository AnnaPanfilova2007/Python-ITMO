import os
import sys
import urllib

from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
import models
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from utilits.currencies_api import get_currencies
from datetime import datetime
import controllers
from typing import Dict, List, Any, Optional

db_controller = controllers.CurrencyRatesCRUD(None)
currency_controller = controllers.CurrencyController(db_controller)
pages_controller = controllers.PagesController()
try:
    db_controller._create()
    print("База данных инициализирована")
except Exception as e:
    print(f"Ошибка инициализации БД: {e}")


url_query_dict: Dict[str, List[str]]
m_autor = models.Author('Anna Panfilova', 'P3121', "https://github.com/AnnaPanfilova2007/Python-ITMO/tree/main/Laboratory%20work%208")
m_app = models.App("Приложение для\nотслеживания\nкурса валют", "1.0", m_autor)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global m_autor, m_app, url_query_dict

        try:
            parsed_path = urlparse(self.path)
            path = parsed_path.path
            query_params = parse_qs(parsed_path.query)

            # Логирование запроса
            print(f"Запрос: {path}, Параметры: {query_params}")

            # Маршрутизация
            if path == '/':
                self.handle_main_page()
            elif path == '/users':
                self.handle_users_list()
            elif path == '/user':
                self.handle_user(query_params)
            elif path == '/currencies':
                self.handle_currencies_list(query_params)
            elif path == '/currency/delete':
                self.handle_currency_delete(query_params)
            elif path == '/author':
                self.handle_author_info()
            else:
                self.send_error(404, "Страница не найдена")

        except Exception as e:
            print(f"Ошибка обработки запроса: {e}")
            self.send_error(500, f"Внутренняя ошибка: {str(e)}")

    def handle_main_page(self):
        """Обработка главной страницы"""
        try:
            # Получаем список валют через CurrencyController
            currencies = currency_controller.list_currencies()

            # Форматируем данные для отображения (берем только 5 первых)
            display_currencies = []
            if currencies and isinstance(currencies, list):
                for i, currency in enumerate(currencies[:5]):
                    if isinstance(currency, dict):
                        display_currencies.append({
                            'id': currency.get('id'),
                            'code': currency.get('chc', currency.get('code', '')),
                            'name': currency.get('name_v', currency.get('name', '')),
                            'value': currency.get('value', 0),
                            'nominal': currency.get('nominal', 1)
                        })

            # Используем PagesController для рендеринга
            html = pages_controller.render_index(
                currencies=display_currencies,
                author_name=m_autor.name,
                group=m_autor.group,
                app_name=m_app.name,
                version=m_app.version
            )

            self.send_html_response(html)

        except Exception as e:
            print(f"Ошибка главной страницы: {e}")
            self.send_error(500, "Не удалось загрузить главную страницу")

    def handle_users_list(self):
        template = env.get_template("users.html")
        # Получаем список пользователей из контроллера
        users: List[Dict[str, Any]] = currency_controller.get_users()
        # Рендерим страницу пользователей
        result = pages_controller.render_users(m_app.name, users)
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(result.encode('utf-8'))

    def handle_user(self, query_params):
        if 'id' in query_params:
            try:
                user_id: int = int(url_query_dict['id'][0])
                # Получаем данные пользователя по ID
                user: Optional[Dict[str, Any]] = currency_controller.get_user(user_id)

                if user:
                    user_currencies: List[Dict[str, Any]] = currency_controller.get_user_currencies(user_id)
                    # Рендерим страницу пользователя
                    result = pages_controller.render_user(m_app.name, user, user_currencies)
                    template_user = env.get_template("user_detail.html")

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

    def handle_currencies_list(self):
        """Обработка списка валют с возможностью обновления"""
        try:
            # Обработка обновления курсов валют из параметров запроса
            result_msg = ""
            for param, values in query_params.items():
                if len(param) == 3 and values:  # Код валюты из 3 букв
                    try:
                        value = float(values[0])
                        # Используем CurrencyController для обновления
                        currency_controller.update_currency(param, value)
                        result_msg = f"Курс {param} обновлен на {value}"
                    except (ValueError, TypeError) as e:
                        result_msg = f"Ошибка обновления {param}: {e}"
                    except Exception as e:
                        result_msg = f"Ошибка обновления {param}: {str(e)}"

            # Получаем список всех валют через CurrencyController
            currencies = currency_controller.list_currencies()

            # Форматируем данные для отображения
            formatted_currencies = []
            if currencies and isinstance(currencies, list):
                for currency in currencies:
                    if isinstance(currency, dict):
                        formatted_currencies.append({
                            'id': currency.get('id'),
                            'code': currency.get('chc', currency.get('code', '')),
                            'name': currency.get('name_v', currency.get('name', '')),
                            'value': currency.get('value', 0),
                            'nominal': currency.get('nominal', 1)
                        })

            # Используем PagesController для рендеринга
            html = pages_controller.render_currencies(
                app_name=m_app.name,
                currencies=formatted_currencies,
                result=result_msg
            )

            self.send_html_response(html)

        except Exception as e:
            print(f"Ошибка страницы валют: {e}")
            self.send_error(500, "Не удалось загрузить список валют")


    def handle_author_info(self):
        template = env.get_template("author.html")
        result = pages_controller.render_author(
            m_autor.name,
            m_autor.group,
            m_app.name,
            m_app.version
        )
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(result.encode('utf-8'))

    def send_html_response(self, html: str, status_code: int = 200):
        """Отправка HTML ответа"""
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(html.encode('utf-8'))))
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, "templates")
env = Environment(
    loader=FileSystemLoader(template_dir),
    autoescape=select_autoescape()
)

if __name__ == '__main__':
    print('server is running')
    httpd = HTTPServer(('localhost', 8800), SimpleHTTPRequestHandler)
    httpd.serve_forever()