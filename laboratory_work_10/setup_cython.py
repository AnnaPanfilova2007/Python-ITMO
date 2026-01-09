from Cython.Build import cythonize
from setuptools import setup

setup(
    ext_modules=cythonize("Cython_int.pyx", annotate=True, compiler_directives={"language_level": 3}),
)
