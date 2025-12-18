from jinja2 import Environment, PackageLoader, select_autoescape
from models import Author
from controllers import databasecontroller
from controllers import CurrencyRatesCRUD
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse


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
            self.handle_user_detail(query_params)
        elif path == '/currencies':
            self.handle_currencies_list()
        elif path == '/author':
            self.handle_author_info()
        else:
            self.send_error(404, "Страница не найдена")

    def handle_author_info(self):
        m_autor = Author('Anna Panfilova', 'P3121')
        template = env.get_template("index.html")
        result = template.render(myapp="CurrenciesListApp",
                                 navigation=[{'caption': 'Основная страница',
                                              'href': "http://localhost:8080/",
                                              'githab': 'https://github.com/AnnaPanfilova2007/Python-ITMO',
                                              }],
                                 author_name=m_autor.name,
                                 group=m_autor.group

                                 )
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