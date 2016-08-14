# -*- coding: utf-8 -*-
"""
"""
from distutils.core import setup

from distutils.extension import Extension
from Cython.Build import cythonize


ext = [
    Extension(
        'pywbxml',
        ['pywbxml.pyx'],
        library_dirs=['./', './wbxmldist/lib/'],
        include_dirs=['./wbxmldist/include/libwbxml-1.0/wbxml/'],
        )
    ]


setup(
  name='libwbxml python wrapper',
  ext_modules=cythonize(ext, force=True, language_level=3),
)
