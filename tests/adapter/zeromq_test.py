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
import mox

##
# ZeroMQ modules
import zmq

##
# promise modules
from promise import Deferred

##
# pygrapes modules
#
from pygrapes.adapter import Zmq


class ZmqAdapterTestCase(unittest.TestCase):

    def setUp(self):
        self.mox = mox.Mox()
        self.ctx = self.mox.CreateMock(zmq.Context)

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_init_expects_no_args(self):
        self.assertFalse(Zmq() is None)

    def test_init_allows_to_pass_config_arg(self):
        self.assertFalse(Zmq(config={}) is None)



if "__main__" == __name__:
    unittest.main()
