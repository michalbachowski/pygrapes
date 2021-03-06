#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# python standard library
#
import unittest

##
# pygrapes modules
#
from pygrapes.serializer import MsgPack


class MsgPackSerializerTestCase(unittest.TestCase):

    def test_method_dumps_exists(self):
        self.assertTrue(hasattr(MsgPack(), 'dumps'))

    def test_method_dumps_expects_one_arg(self):
        self.assertRaises(TypeError, MsgPack().dumps)

    def test_dumps_return_string(self):
        self.assertTrue(isinstance(MsgPack().dumps([1,3,2]), bytes))

    def test_method_loads_exists(self):
        self.assertTrue(hasattr(MsgPack(), 'loads'))

    def test_method_loads_expects_one_arg(self):
        self.assertRaises(TypeError, MsgPack().loads)

    def test_loads_return_object(self):
        self.assertTrue(isinstance(MsgPack().loads(MsgPack().dumps([1,3,2])),
            list))


if "__main__" == __name__:
    unittest.main()
