import sys
from functools import lru_cache
from queue import Queue
import matplotlib.pyplot as plt
from numpy.ma.extras import average
import timeit


@lru_cache(None)
def build_tree_recursive_cash(height: int, root: int, l_l=lambda x: x ** 2, l_r=lambda x: x ** 2 + 2):
    """Рекурсивно с помощью кеша генерирует бинарное дерево в виде словарей.

    Строит дерево с помощью рекурсии, каждый узел которой - словарь

    Args:
        height: Высота дерева
        root: целое число
        l_l: Функция для вычисления левых веток
        l_r: Функция для вычисления правых веток

    Returns:
        Словарь, где ключами являются значения root, а значениями - список результатов работы функции

    """
    if height < 1:
        return {str(root): []}
    return {str(root): [build_tree_recursive_cash(height - 1, l_l(root), l_l, l_r),
                        build_tree_recursive_cash(height - 1, l_r(root), l_l, l_r)]}


@lru_cache(None)
def build_tree_iterative_cach(height: int, root: int, l_b=lambda x: x ** 2, r_b=lambda x: x ** 2 + 2):
    """
    Создает бинарное дерево заданной высоты c , используя алгоритм поиска в ширину.
    Узлы обрабатываются уровень за уровнем с помощью очереди.
    А так же используя кеш

    Args:
        height (int): Высота генерируемого бинарного дерева
        root (int): Значение корневого узла дерева
        l_b (callable, optional): Функция для вычисления левого потомка.
                                 По умолчанию x**2.
        r_b (callable, optional): Функция для вычисления правого потомка.
                                 По умолчанию x**2 + 2.

    Returns:
        dict: Словарь, представляющий бинарное дерево в формате:
              {root_value: [left_subtree, right_subtree]}
    """
    queue = Queue()
    di = {str(root): []}
    queue.put(di)
    for i in range(2 ** height - 1):
        current = queue.get()
        for key in current:
            l_di = {str(l_b(int(key))): []}
            r_di = {str(r_b(int(key))): []}
            current[key] += [l_di, r_di]
            queue.put(l_di)
            queue.put(r_di)
    return di

def time(func, n, repeat=10):
    """Возвращает среднее время выполнения func(n)"""
    times = timeit.repeat(lambda: func(n, 11), number=5, repeat=repeat)
    return average(times)

def main():
    test_data = list(range(1, 10, 1))

    res_recursive_cached = []
    res_iterative_cached = []

    for n in test_data:
        res_recursive_cached.append(time(build_tree_recursive_cash, n))
        res_iterative_cached.append(time(build_tree_iterative_cach, n))

    # С кэшем
    plt.plot(test_data, res_recursive_cached, label="Рекурсивный с кэшем")
    plt.plot(test_data, res_iterative_cached, label="Итеративный с кэшем")
    plt.xlabel("высота дерева")
    plt.suptitle("Сравнение рекурсивного и итеративного факториала с кешем")
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
