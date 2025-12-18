from setuptools import setup
from Cython.Build import cythonize
import os
print(os.environ["PATH"])
setup(
    ext_modules=cythonize("Cython_int.pyx", annotate=True, compiler_directives={"language_level": 3}),
)
