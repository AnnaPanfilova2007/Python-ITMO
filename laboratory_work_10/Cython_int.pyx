# cython: language_level=3
# distutils: language=c
import Cython

def integrate_basic(f, double a, double b, *,int n_iter = 100000):
    if n_iter <= 0:
        raise ValueError("n_iter не может быть <= 0")

    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    cdef double x

    for i in range(n_iter):
        x = a + i * step
        acc += f(x) * step
        return acc