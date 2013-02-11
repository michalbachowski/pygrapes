#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# python standard library
#
import unittest
import mox

# hack for loading modules
import _path
_path.fix()

##
# pygrapes modules
#
from pygrapes import Foo


class FooTestCase(unittest.TestCase):

    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()


if "__main__" == __name__:
    unittest.main()
