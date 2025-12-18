import math
import doctest
import concurrent.futures as ftres
from functools import partial
from typing import Callable
import concurrent.futures as futures

import numba


# итерация 1
def integrate(f: Callable, a:float, b:float, *, n_iter=100000)-> float:
    """
      Вычисляет приближённое значение определённого интеграла функции
      методом левых прямоугольников (Left Riemann Sum).

      Этот метод аппроксимирует площадь под кривой f(x) на отрезке [a, b]
      суммой площадей прямоугольников, где высота каждого прямоугольника
      равна значению функции в левой точке соответствующего подинтервала.

      Параметры
      ----------
      f : Callable
          Интегрируемая функция одного вещественного аргумента,
          возвращающая вещественное значение.
      a : float
          Нижний предел интегрирования (левая граница отрезка).
      b : float
          Верхний предел интегрирования (правая граница отрезка).
      n_iter : int, optional
          Количество подинтервалов для разбиения отрезка [a, b].
          Большее значение увеличивает точность вычислений,
          но требует больше вычислительных ресурсов.
          По умолчанию 100000.

      Возвращаемое значение
      -------
      float
          Приближённое значение определённого интеграла ∫[a, b] f(x) dx.

    doctest:

    >>> integrate(math.sin, -math.pi/2, math.pi/2, n_iter=5000)
    -0.0006283185
    >>> integrate(quadratic, 0, 1, n_iter=5000)
    0.16676668
      """

    if n_iter <= 0:
        raise ValueError("n_iter не может быть <= 0")
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i*step) * step
    return round(acc, 10)


#итерация 2 потоки
def integrate_async(f: Callable, a:float, b:float, *, n_iter=100000, n_jobs = 3)-> float:
    """
    Вычисляет приближённое значение определённого интеграла функции
    методом левых прямоугольников с использованием пула потоков (ThreadPoolExecutor).

    Параметры
    ----------
    f : Callable[[float], float]
        Интегрируемая функция одного вещественного аргумента.
    a : float
        Нижний предел интегрирования (левая граница интервала).
    b : float
        Верхний предел интегрирования (правая граница интервала).
    n_iter : int, optional
        Общее количество подинтервалов для разбиения отрезка [a, b].
        По умолчанию 100000.
    n_jobs : int, optional
        Количество потоков в пуле для параллельных вычислений.
        По умолчанию 3.

    Возвращаемое значение
    -------
    float
        Приближённое значение определённого интеграла ∫[a, b] f(x) dx,
        округлённое до 10 знаков после запятой.

    >>> integrate_async(math.sin, -math.pi/2, math.pi/2, n_iter=5000)
    -0.00062857
    >>> integrate_async(quadratic, 0, 1, n_iter=5000)
    0.16676672
    """

    executor = ftres.ThreadPoolExecutor(max_workers=n_jobs)
    spawn = partial(executor.submit, integrate, f, n_iter = n_iter // n_jobs)
    step = (b - a) / n_jobs
    fs = [spawn(a + i * step, a + (i + 1) * step) for i in range(n_jobs)]
    return round(sum(list(f.result() for f in ftres.as_completed(fs))), 10)

#итерация 3 через процессы
def integrate_process(func: Callable, a: float, b: float, *, n_iter: int = 100000, n_jobs: int = 2) -> float:
    """
        Вычисляет приближённое значение определённого интеграла функции
        методом левых прямоугольников с использованием параллельных процессов.

        Параметры
        ----------
        func : Callable[[float], float]
            Интегрируемая функция одного вещественного аргумента.
            Должна принимать float и возвращать float.

        a : float
            Нижний предел интегрирования (левая граница интервала).

        b : float
            Верхний предел интегрирования (правая граница интервала).
            Если a > b, интеграл вычисляется в обратном направлении
            и результат будет отрицательным.

        n_iter : int, опционально
            Общее количество подинтервалов для разбиения отрезка [a, b].
            Распределяется равномерно между всеми процессами.
            По умолчанию: 100000.

        n_jobs : int, опционально
            Количество процессов для параллельных вычислений.
            Если n_jobs = 1, вычисления выполняются последовательно.
            Рекомендуется устанавливать равным количеству ядер CPU.
            По умолчанию: 2.

        Возвращаемое значение
        -------
        float
            Приближённое значение определённого интеграла ∫[a, b] func(x) dx.

        doctest:

        >>> integrate_process(math.sin, -math.pi/2, math.pi/2, n_iter=5000)
        -0.0006283186
        >>> integrate_process(quadratic, 0, 1, n_iter=5000)
        0.16676668
        """
    iter_per_job = n_iter // n_jobs
    with futures.ProcessPoolExecutor(max_workers=n_jobs) as executor:
        threadStart = partial(executor.submit, integrate, func, n_iter=iter_per_job)

        step = (b - a) / n_jobs
        results = [threadStart(a + i * step, a + (i + 1) * step) for i in range(n_jobs)]
        return round(sum([i.result() for i in futures.as_completed(results)]), 10)

#интеграция 5 через nogil
def integrate_async_nogil(f: Callable, a:float, b:float, *, n_iter=100000, n_jobs = 3)-> float:
    """
    Вычисляет приближённое значение определённого интеграла функции
    методом левых прямоугольников с использованием пула потоков (ThreadPoolExecutor).

    Параметры
    ----------
    f : Callable[[float], float]
        Интегрируемая функция одного вещественного аргумента.
    a : float
        Нижний предел интегрирования (левая граница интервала).
    b : float
        Верхний предел интегрирования (правая граница интервала).
    n_iter : int, optional
        Общее количество подинтервалов для разбиения отрезка [a, b].
        По умолчанию 100000.
    n_jobs : int, optional
        Количество потоков в пуле для параллельных вычислений.
        По умолчанию 3.

    Возвращаемое значение
    -------
    float
        Приближённое значение определённого интеграла ∫[a, b] f(x) dx,
        округлённое до 10 знаков после запятой.

    >>> integrate_async(math.sin, -math.pi/2, math.pi/2, n_iter=5000)
    -0.00062857
    >>> integrate_async(quadratic, 0, 1, n_iter=5000)
    0.16676672
    """
    integrate_async_nogil = numba.jit(integrate, nogil=True)
    executor = ftres.ThreadPoolExecutor(max_workers=n_jobs)
    spawn = partial(executor.submit, integrate, f, n_iter = n_iter // n_jobs)
    step = (b - a) / n_jobs
    fs = [spawn(a + i * step, a + (i + 1) * step) for i in range(n_jobs)]
    return round(sum(list(f.result() for f in ftres.as_completed(fs))), 10)


def quadratic(x):
    return 2*x**2 - 3*x + 1

if __name__ == "__main__":
    doctest.testmod(verbose=True)
    print(integrate_process(lambda x: x, 0, 1,
                                   n_iter=5000, n_jobs=1))

