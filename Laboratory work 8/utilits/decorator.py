import logging
import sys
import io
from functools import wraps
from typing import Callable

def logger(func = None, *, handle = sys.stdout):
    """
        Декоратор для логирования вызовов функций и их результатов.

        Параметры
        ---------
        func : Callable, optional
            Декорируемая функция. Если None, декоратор используется с аргументами.
        handle : IO или logging.Logger, по умолчанию sys.stdout
            Обработчик для вывода логов. Может быть:
            - Объектом ввода-вывода (sys.stdout, sys.stderr, io.StringIO и т.д.)
            - Объектом logging.Logger для интеграции с модулем logging

        Возвращает
        ----------
        Обёрнутая функция с логированием.
        """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            is_stringio = (
                    isinstance(handle, io.StringIO) and
                    handle is not sys.stdout and
                    handle is not sys.stderr
            )
            args_rep = [repr(arg) for arg in args]
            kwargs_rep = [f"{key}={repr(value)}" for key, value in kwargs.items()]
            log_massage = f"Вызов функции {f.__name__}\n"
            if isinstance(handle, logging.Logger):
                handle.info(log_massage)
            else:
                # Варианты 1 и 2: Используем .write()
                handle.write(log_massage)
                if hasattr(handle, 'flush'):
                    handle.flush()

            try:
                res = f(*args, **kwargs)
                full_massage = log_massage + f"функция {f.__name__} выполнена без исключений\nresult:{res}"
                if isinstance(handle, logging.Logger):#проверка пренадлежит ли handle классу Logger
                    handle.info(full_massage)
                else:
                    handle.write(full_massage)
                    if hasattr(handle, 'flush'):#проверяет присутствует ли атрибут у объекта
                        handle.flush()#позволяет записывать данные из временного хранилища
                if is_stringio:
                    # Сохраняем текущую позицию
                    current_pos = handle.tell()
                    handle.seek(0)
                    content = handle.read()
                    print(content, end="")
                    # Возвращаем позицию для продолжения записи
                    handle.seek(current_pos)
                return res
            except Exception as e:
                err_massage = f"{f.__name__} совершена с исключением: {type(e).__name__}: {e}\n"
                full_massage = log_massage+err_massage
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
        return wrapper
    if func is None:
        return decorator
    else:
        return decorator(func)




