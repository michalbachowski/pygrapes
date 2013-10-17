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
    packages=['pygrapes', 'pygrapes.adapter', 'pygrapes.serializer'],
    package_dir={'': 'src', 'adatper': 'src/adapter',
        'serializer': 'src/serializer'},
    install_requires=['PyPromise==1.1.1', 'msgpack-python>=0.3.0'],
    dependency_links = ['http://github.com/michalbachowski/pypromise/archive/1.1.1.zip#egg=PyPromise-1.1.1'])
