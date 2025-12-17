import logging
import sys
import io
from functools import wraps
from typing import Callable, Any


class WarrningError(Exception):
    """
    Исключение уровня WARNING для некритичных ошибок.
    """
    def __init__(self, text: str, res: Any):
        Exception.__init__(self, text)
        self.res = res


class CriticalError(Exception):
    """
    Исключение уровня CRITICAL для фатальных ошибок.
    """

    def __init__(self, text: str):
        Exception.__init__(self, text)


def logger(func=None, *, handle=sys.stdout):
    """
       Исключение уровня WARNING для некритичных ошибок.

       Используется для обработки ситуаций, которые не требуют
       прерывания выполнения программы, но требуют уведомления.

       Атрибуты
       --------
       text : str
           Сообщение об ошибке.
       res : Any
           Результат, который можно вернуть несмотря на ошибку.
       """

    def __init__(self, text: str, res: Any):
        Exception.__init__(self, text)
        self.res = res


class CriticalError(Exception):
    """
    Исключение уровня CRITICAL для фатальных ошибок.

    Используется для обработки ситуаций, которые требуют
    немедленного прерывания выполнения программы.

    Атрибуты
    --------
    text : str
        Сообщение об ошибке.
    """

    def __init__(self, text: str):
        Exception.__init__(self, text)


def logger(func=None, *, handle=sys.stdout):
    """
    Декоратор для логирования решения квадратных уравнений.

    Параметры
    ---------
    func : Callable, optional
        Декорируемая функция. Должна принимать 3 аргумента: a, b, c.
    handle : typing.IO или logging.Logger, по умолчанию sys.stdout
        Обработчик для вывода логов. Поддерживает:
        - Стандартные потоки (sys.stdout, sys.stderr)
        - Объекты io.StringIO
        - Объекты logging.Logger

    Возвращает
    ----------
    Обёрнутая функция с расширенным логированием.

    """
    inf: Callable = None
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            is_stringio = (
                    isinstance(handle, io.StringIO) and
                    handle is not sys.stdout and
                    handle is not sys.stderr
            )
            arg = [ int(arg) for arg in args]
            log_massage = f"Вызов функции Solving equation: {arg[0]}x^2 + {arg[1]}x + {arg[2]} = 0"

            if isinstance(handle, logging.Logger):
                handle.info(log_massage)
            else:
                # Варианты 1 и 2: Используем .write()
                handle.write(log_massage)
                if hasattr(handle, 'flush'):
                    handle.flush()
            res = None
            try:
                res = f(*args, **kwargs)
                if res == None:
                    handle.warning('')
                full_massage = f"функция {f.__name__} выполнена без исключений"
                if isinstance(handle, logging.Logger):  # проверка пренадлежит ли handle классу Logger
                    handle.info(full_massage)
                else:
                    handle.write(full_massage)
                    if hasattr(handle, 'flush'):  # проверяет присутствует ли атрибут у объекта
                        handle.flush()  # позволяет записывать данные из временного хранилища
                if is_stringio:
                    # Сохраняем текущую позицию
                    current_pos = handle.tell()
                    handle.seek(0)
                    content = handle.read()
                    print(content, end="")
                    # Возвращаем позицию для продолжения записи
                    handle.seek(current_pos)
                return res
            except WarrningError as e:
                handle.warning(e)
                return e.res
            except CriticalError as e:
                handle.critical(e)
                raise e
            except Exception as e:
                err_massage = f"{f.__name__} совершена с исключением: {type(e).__name__}: {e}\n"
                full_massage = log_massage + err_massage
                if isinstance(handle, logging.Logger):
                    handle.error(full_massage)
                else:
                    handle.write(full_massage)
                    if hasattr(handle, "flush"):
                        handle.flush()
                if is_stringio:
                    # Сохраняем текущую позицию
                    current_pos = handle.tell()
                    handle.seek(0)
                    content = handle.read()
                    print(content, end="")
                    # Возвращаем позицию для продолжения записи
                    handle.seek(current_pos)
                raise
            finally:
                if res == None:
                    pass
                else:
                    handle.info(res)

        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)
