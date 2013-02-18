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
# pygrapes modules
#
from pygrapes.adapter import Local


class LocalAdapterTestCase(unittest.TestCase):
    
    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_detach_listener_raises_KeyError_when_route_does_not_exist(self):
        l = Local()
        self.assertRaises(KeyError, partial(l.detach_listener, 'foo'))

    def test_send_raises_KeyError_when_route_has_no_handler(self):
        l = Local()
        self.assertRaises(KeyError, partial(l.send, 'foo', '', None))

    def test_send_calls_attached_callback(self):
        c = self.mox.CreateMockAnything()
        c('asd', deferred='foo')
        self.mox.ReplayAll()

        l = Local()
        l.attach_listener('foo', c)
        l.send('foo', 'asd', 'foo')

        self.mox.VerifyAll()

    def test_attach_listener_overrides_handlers(self):
        c_not_called = self.mox.CreateMockAnything()
        c = self.mox.CreateMockAnything()
        c('asd', deferred='foo')
        self.mox.ReplayAll()

        l = Local()
        l.attach_listener('foo', c_not_called)
        l.attach_listener('foo', c)
        l.send('foo', 'asd', 'foo')

        self.mox.VerifyAll()

    def test_implements_all_methods_from_abstract_class(self):
        self.assertTrue(hasattr(Local(), 'serve'))
        self.assertTrue(hasattr(Local(), 'connect'))
        self.assertTrue(hasattr(Local(), 'send'))
        self.assertTrue(hasattr(Local(), 'ack'))
        self.assertTrue(hasattr(Local(), 'attach_listener'))
        self.assertTrue(hasattr(Local(), 'detach_listener'))

if "__main__" == __name__:
    unittest.main()
