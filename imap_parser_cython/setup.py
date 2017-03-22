# -*- coding: utf-8 -*-
"""
"""

from distutils.core import setup, Extension
from Cython.Build import cythonize


ext = [
    Extension(
        "pyimapparser",
        sources=["pyimapparser.pyx"],
        language="c++",
        extra_compile_args=['-g', '-std=c++11']
    )
]


setup(
  name='imap response parser python wrapper',
  ext_modules=cythonize(ext, force=True, language_level=3),
)
