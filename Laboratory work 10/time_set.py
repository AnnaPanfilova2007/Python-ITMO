import math
import timeit
from numpy.ma.extras import average
from main import *
import matplotlib.pyplot as plt
from Cython_int import integrate_basic

def time(func, n, repeat=10):
    """Возвращает среднее время выполнения func(n)"""
    times = timeit.repeat(lambda: func(math.cos, 0, math.pi, n_iter = n), number=5, repeat=repeat)
    return average(times)

if __name__ == "__main__":
    test_data = list(range(1000, 10000, 1000))

    res_integraton = []
    res_integraton_async = []
    res_integraton_process = []
    res_integraton_cython = []

    for n in test_data:
        res_integraton.append(time(integrate, n))
        res_integraton_async.append(time(integrate_async, n))
        res_integraton_process.append(time(integrate_process, n))
        res_integraton_cython.append(time(integrate_basic, n))

    fig, axes = plt.subplots(1, 4, figsize=(10, 8))
    axes[0].plot(test_data,res_integraton, 'r-')
    axes[0].set_title('Integration')
    axes[0].set_ylabel('время')
    axes[0].set_xlabel('количество итераций')
    axes[0].grid(True)

    axes[1].plot(test_data,res_integraton_async, 'r-')
    axes[1].set_title('Integration Async')
    axes[1].set_ylabel('время')
    axes[1].set_xlabel('количество итераций')
    axes[1].grid(True)

    axes[2].plot(test_data,res_integraton_process, 'r-')
    axes[2].set_title('Integration Process')
    axes[2].set_ylabel('время')
    axes[2].set_xlabel('количество итераций')
    axes[2].grid(True)

    axes[3].plot(test_data,res_integraton_cython, 'r-')
    axes[3].set_title('Integration cython')
    axes[3].set_ylabel('время')
    axes[3].set_xlabel('количество итераций')
    axes[3].grid(True)

    plt.tight_layout()
    plt.savefig('time.pdf')

