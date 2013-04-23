#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

# monkey patch os.link to force using symlinks
import os
del os.link

setup(name='PyGrapes',\
    version='0.1.0',\
    description='Distributed Task Framework',\
    license='New BSD License',\
    author='Michał Bachowski',\
    author_email='michal@bachowski.pl',\
    package_dir={'': 'src'},\
    py_modules=['pygrapes'])
