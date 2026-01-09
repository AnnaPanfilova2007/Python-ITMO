import math
import timeit
from main import *
from Cython_int import integrate_basic
from numpy.ma.extras import average

def time(func, n, repeat=10):
    """Возвращает среднее время выполнения func(n)"""
    times = timeit.repeat(lambda: func(math.cos, 0, math.pi, n_iter = n), number=5, repeat=repeat)
    return average(times)

if __name__ == "__main__":
    test_data = 1000
    print(time(integrate, test_data))
    print(time(integrate_async, test_data))
    print(time(integrate_process, test_data))
    print(time(integrate_async_nogil, test_data))
    print(time(integrate_basic, test_data))

