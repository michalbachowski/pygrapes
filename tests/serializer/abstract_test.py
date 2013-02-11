#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# hack for loading modules
#
import _path
_path.fix()

##
# python standard library
#
from functools import partial
import unittest

##
# pygrapes modules
#
from pygrapes.serializer import Base


class BaseSerializerTestCase(unittest.TestCase):

    def test_method_dumps_exists(self):
        self.assertTrue(hasattr(Base(), 'dumps'))

    def test_method_dumps_expects_one_arg(self):
        self.assertRaises(TypeError, Base().dumps)

    def test_dumps_method_must_be_implemented(self):
        self.assertRaises(NotImplementedError, partial(Base().dumps, 1))

    def test_method_loads_exists(self):
        self.assertTrue(hasattr(Base(), 'loads'))

    def test_method_loads_expects_one_arg(self):
        self.assertRaises(TypeError, Base().loads)

    def test_loads_method_must_be_implemented(self):
        self.assertRaises(NotImplementedError, partial(Base().loads, 1))


if "__main__" == __name__:
    unittest.main()
