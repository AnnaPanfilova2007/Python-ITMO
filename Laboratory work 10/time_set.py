import math
import timeit
from numpy.ma.extras import average
from main import *
import matplotlib.pyplot as plt

def time(func, n, repeat=10):
    """Возвращает среднее время выполнения func(n)"""
    times = timeit.repeat(lambda: func(math.cos, 0, math.pi, n_iter = n), number=5, repeat=repeat)
    return average(times)

if __name__ == "__main__":
    test_data = list(range(1000, 10000, 1000))

    res_integraton = []
    res_integraton_async = []
    res_integraton_process = []
    res_integraton_nogil = []

    for n in test_data:
        res_integraton.append(time(integrate, n))
        res_integraton_async.append(time(integrate, n))
        res_integraton_process.append(time(integrate, n))
        res_integraton_nogil.append(time(integrate, n))

    fig, axes = plt.subplots(1, 4, figsize=(10, 8))
    axes[0].plot(res_integraton, test_data, 'r-')
    axes[0].set_title('Integration')
    axes[0].set_xlabel('время')
    axes[0].set_ylabel('количество итераций')
    axes[0].grid(True)

    axes[1].plot(res_integraton_async, test_data, 'r-')
    axes[1].set_title('Integration Async')
    axes[1].set_xlabel('время')
    axes[1].set_ylabel('количество итераций')
    axes[1].grid(True)

    axes[2].plot(res_integraton_process, test_data, 'r-')
    axes[2].set_title('Integration Process')
    axes[2].set_xlabel('время')
    axes[2].set_ylabel('количество итераций')
    axes[2].grid(True)

    axes[3].plot(res_integraton_nogil, test_data, 'r-')
    axes[3].set_title('Integration nogil')
    axes[3].set_xlabel('время')
    axes[3].set_ylabel('количество итераций')
    axes[3].grid(True)

    plt.tight_layout()
    plt.show()

