#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# python standard library
#
import unittest

##
# pygrapes modules
#
from pygrapes.serializer import Json


class JsonSerializerTestCase(unittest.TestCase):

    def test_method_dumps_exists(self):
        self.assertTrue(hasattr(Json(), 'dumps'))

    def test_method_dumps_expects_one_arg(self):
        self.assertRaises(TypeError, Json().dumps)

    def test_dumps_return_string(self):
        self.assertTrue(isinstance(Json().dumps([1,3,2]), str))

    def test_method_loads_exists(self):
        self.assertTrue(hasattr(Json(), 'loads'))

    def test_method_loads_expects_one_arg(self):
        self.assertRaises(TypeError, Json().loads)

    def test_loads_return_object(self):
        self.assertTrue(isinstance(Json().loads('[1,3,2]'), list))


if "__main__" == __name__:
    unittest.main()
