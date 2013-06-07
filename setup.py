#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

# monkey patch os.link to force using symlinks
import os
del os.link

setup(name='PyGrapes',
    url='https://github.com/michalbachowski/pygrapes',
    version='0.1.0',
    description='Distributed Task Framework',
    license='New BSD License',
    author='Michał Bachowski',
    author_email='michal@bachowski.pl',
    packages=['pygrapes'],
    package_dir={'': 'src'},
    install_requires=['PyPromise==1.0.3', 'msgpack-python'],
    dependency_links = ['http://github.com/michalbachowski/pypromise/archive/1.0.3.zip#egg=PyPromise-1.0.3'])
