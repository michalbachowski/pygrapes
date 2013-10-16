#!/usr/bin/env python
# -*- coding: utf-8 -*-

# hack for loading modules

##
# python standard library
#
import collections
import unittest

##
# pygrapes modules
#
from pygrapes.util import not_implemented


class UtilTestCase(unittest.TestCase):

    def test_not_implemented_expects_one_arg(self):
        self.assertRaises(TypeError, not_implemented)

    def test_not_implemented_returns_callable(self):
        self.assertTrue(isinstance(not_implemented(None), collections.Callable))

    def test_not_implemented_callable_raises_runtime_error(self):
        self.assertRaises(RuntimeError, not_implemented(None))

    def test_not_implemented_callable_raises_exception_with_given_message(self):
        try:
            not_implemented('foo')()
        except RuntimeError as e:
            msg = e.args[0]
        else:
            msg = 'bar'

        self.assertEqual('foo', msg)


if "__main__" == __name__:
    unittest.main()
