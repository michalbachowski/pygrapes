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
from pygrapes.adapter import Abstract


class AbstractAdapterTestCase(unittest.TestCase):

    def test_init_requires_no_args(self):
        self.assertFalse(Abstract() is None)

    def test_init_accepts_any_args(self):
        self.assertFalse(Abstract(1,2,3, c='4') is None)

    def test_method_serve_exists(self):
        self.assertTrue(hasattr(Abstract(), 'serve'))

    def test_method_serve_expects_no_args(self):
        Abstract().serve()

    def test_method_send_may_be_implemented(self):
        self.assertEquals(Abstract().serve(), None)

    def test_method_send_exists(self):
        self.assertTrue(hasattr(Abstract(), 'send'))

    def test_method_send_expects_3_args_1(self):
        self.assertRaises(TypeError, Abstract().send)

    def test_method_send_expects_3_args_2(self):
        self.assertRaises(TypeError, partial(Abstract().send, None))

    def test_method_send_expects_3_args_3(self):
        self.assertRaises(TypeError, partial(Abstract().send, None, None))

    def test_method_send_must_be_implemented(self):
        self.assertRaises(NotImplementedError, \
                partial(Abstract().send, None, None, None))

    def test_method_attach_listener_exists(self):
        self.assertTrue(hasattr(Abstract(), 'attach_listener'))

    def test_method_attach_listener_expects_2_args_1(self):
        self.assertRaises(TypeError, Abstract().attach_listener)

    def test_method_attach_listener_expects_2_args_2(self):
        self.assertRaises(TypeError, partial(Abstract().attach_listener, None))

    def test_attach_listener_method_is_implemented(self):
        self.assertFalse(Abstract().attach_listener(None, None) is None)

    def test_attach_listener_returns_instance_of_abstract(self):
        self.assertTrue(isinstance(Abstract().attach_listener(None, None),
            Abstract))

    def test_method_detach_listener_exists(self):
        self.assertTrue(hasattr(Abstract(), 'detach_listener'))

    def test_method_detach_listener_expects_one_arg(self):
        self.assertRaises(TypeError, Abstract().detach_listener)

    def test_detach_listener_is_implemented(self):
        self.assertRaises(KeyError, partial(Abstract().detach_listener, 1))

    def test_detach_listener_expects_route_to_has_handler_attacher(self):
        a = Abstract().attach_listener('a', None)
        self.assertFalse(a.detach_listener('a') is None)

    def test_detach_listener_returns_instance_of_Abstract(self):
        a = Abstract().attach_listener('a', None)
        self.assertTrue(isinstance(a.detach_listener('a'), Abstract))

    def test_method_ack_exists(self):
        self.assertTrue(hasattr(Abstract(), 'ack'))

    def test_method_ack_expects_one_arg(self):
        self.assertRaises(TypeError, Abstract().ack)

    def test_ack_method_does_not_have_to_be_implemented(self):
        self.assertTrue(Abstract().ack(None) is None)

    def test_method_connect_exists(self):
        self.assertTrue(hasattr(Abstract(), 'connect'))

    def test_connect_method_does_not_have_to_be_implemented(self):
        self.assertTrue(Abstract().connect() is None)


if "__main__" == __name__:
    unittest.main()
