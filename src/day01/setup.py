from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext


extensions = [Extension("_solver", ["_solver.pyx"])]

setup(cmdclass={'build_ext': build_ext},
      ext_modules=cythonize(extensions, language_level=3))

# py .\setup.py build_ext --inplace
