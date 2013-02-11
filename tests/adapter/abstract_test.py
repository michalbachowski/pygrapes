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
from pygrapes.adapter.abstract import Abstract


class AbstractAdapterTestCase(unittest.TestCase):
    
    def test_method_send_exists(self):
        self.assertTrue(hasattr(Abstract(), 'send'))

    def test_method_dumps_expects_3_args_1(self):
        self.assertRaises(TypeError, Abstract().send)

    def test_method_dumps_expects_3_args_2(self):
        self.assertRaises(TypeError, partial(Abstract().send, None))

    def test_method_dumps_expects_3_args_3(self):
        self.assertRaises(TypeError, partial(Abstract().send, None, None))

    def test_send_method_must_be_implemented(self):
        self.assertRaises(NotImplementedError, partial(Abstract().send, None, \
                None, None))

    def test_method_attach_listener_exists(self):
        self.assertTrue(hasattr(Abstract(), 'attach_listener'))

    def test_method_dumps_expects_2_args_1(self):
        self.assertRaises(TypeError, Abstract().attach_listener)

    def test_method_dumps_expects_2_args_2(self):
        self.assertRaises(TypeError, partial(Abstract().attach_listener, None))

    def test_attach_listener_method_must_be_implemented(self):
        self.assertRaises(NotImplementedError, \
                partial(Abstract().attach_listener, None, None))
    
    def test_method_detach_listener_exists(self):
        self.assertTrue(hasattr(Abstract(), 'detach_listener'))

    def test_method_dumps_expects_one_arg(self):
        self.assertRaises(TypeError, Abstract().detach_listener)

    def test_detach_listener_method_must_be_implemented(self):
        self.assertRaises(NotImplementedError, \
                partial(Abstract().detach_listener, 1))

    def test_method_ack_exists(self):
        self.assertTrue(hasattr(Abstract(), 'ack'))

    def test_method_dumps_expects_one_arg(self):
        self.assertRaises(TypeError, Abstract().ack)

    def test_ack_method_does_not_have_to_be_implemented(self):
        self.assertTrue(Abstract().ack(None) is None)


if "__main__" == __name__:
    unittest.main()
