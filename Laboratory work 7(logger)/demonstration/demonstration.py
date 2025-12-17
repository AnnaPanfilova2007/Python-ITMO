from demonstration_decorator import logger
import logging.handlers
import math
from demonstration_decorator import WarrningError
from demonstration_decorator import CriticalError
logging.basicConfig(
    filename="../quadratic.log",
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s"
)
log = logging.getLogger("L1")
handler = logging.handlers.RotatingFileHandler("currency_file_demonstration.txt", encoding="UTF-8")
log.addHandler(handler)
log.setLevel(1)
@logger(handle=log)
def solve_quadratic(a, b, c):
    """
       Решает квадратное уравнение вида ax² + bx + c = 0.

       Вычисляет корни квадратного уравнения с обработкой различных
       сценариев через пользовательские исключения.

       Параметры
       ---------
       a : int или float
           Коэффициент при x².
       b : int или float
           Коэффициент при x.
       c : int или float
           Свободный член.

       Возвращает
       ----------
       tuple
           Кортеж с корнями уравнения:
           - None: если дискриминант отрицательный (WarrningError)
           - (x,): один корень при нулевом дискриминанте
           - (x1, x2): два корня при положительном дискриминанте

       Исключения
       ----------
       TypeError
           Если какой-либо из коэффициентов не является числом.
       CriticalError
           Если коэффициент a равен нулю (не квадратное уравнение).
       WarrningError
           Если дискриминант отрицательный (нет действительных корней).
       """

    # Ошибка типов
    for name, value in zip(("a", "b", "c"), (a, b, c)):
        if not isinstance(value, (int, float)):
            raise TypeError(f"Coefficient '{name}' must be numeric")

    # Ошибка: a == 0
    if a == 0:
        raise CriticalError("a cannot be zero, critical situation")


    d = b*b - 4*a*c
    logging.debug(f"Discriminant: {d}")

    if d < 0:
        raise WarrningError("Discriminant < 0: no real roots", None)

    if d == 0:
        x = -b / (2*a)
        logging.info("One real root")
        return (x,)

    root1 = (-b + math.sqrt(d)) / (2*a)
    root2 = (-b - math.sqrt(d)) / (2*a)
    logging.info("Two real roots computed")
    return root1, root2

if __name__ == "__main__":
    print(solve_quadratic(1, 1, 1))