import timeit
from functools import cache, lru_cache
import matplotlib.pyplot as plt
from numpy.ma.extras import average


def fact_recursive(n: int) -> int:
    """Рекурсивный факториал"""
    if n == 0:
        return 1
    return n * fact_recursive(n - 1)


def fact_iterative(n: int) -> int:
    """Нерекурсивный факториал"""
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res


@lru_cache(None)
def fact_recursive_cash(n: int) -> int:
    """Рекурсивный факториал с кешем"""
    if n == 0:
        return 1
    return n * fact_recursive_cash(n - 1)


@lru_cache(None)
def fact_iterative_cash(n: int) -> int:
    """Нерекурсивный факториал c кешем"""
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res


def time(func, n, repeat=10):
    """Возвращает среднее время выполнения func(n)"""
    times = timeit.repeat(lambda: func(n), number=5, repeat=repeat)
    return average(times)


def main():
    # фиксированный набор данных
    test_data = list(range(10, 300, 10))

    res_recursive = []
    res_iterative = []

    for n in test_data:
        res_recursive.append(time(fact_recursive, n))
        res_iterative.append(time(fact_iterative, n))

    fig, ax = plt.subplots(1, 3)

    # Без кеша
    ax[0].plot(test_data, res_recursive, label="Рекурсивный")
    ax[0].plot(test_data, res_iterative, label="Итеративный")
    ax[0].set(xlabel="n")
    ax[0].set(ylabel="Время (сек)")
    ax[0].legend()

    res_recursive_cached = []
    res_iterative_cached = []

    for n in test_data:
        res_recursive_cached.append(time(fact_recursive_cash, n))
        res_iterative_cached.append(time(fact_iterative_cash, n))

    # С кэшем
    ax[1].plot(test_data, res_recursive_cached, label="Рекурсивный с кэшем")
    ax[1].plot(test_data, res_iterative_cached, label="Итеративный с кэшем")
    ax[1].set(xlabel="n")
    ax[1].set(title="Сравнение рекурсивного и итеративного факториала с кешем")
    ax[1].legend()

    # Заставляем второй график взять масштаб у первого
    ax[1].sharex(ax[0])
    ax[1].sharey(ax[0])

    ax[2].plot(test_data, res_recursive_cached, label="Рекурсивный с кэшем")
    ax[2].plot(test_data, res_iterative_cached, label="Итеративный с кэшем")
    ax[2].set(xlabel="n")
    ax[2].legend()

    plt.show()


if __name__ == '__main__':
    main()
