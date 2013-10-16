#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# test hepers
#
from testutils import mock, IsA, IsCallable

##
# python standard library
#
from functools import partial
import unittest


##
# pygrapes modules
#
from pygrapes.adapter import Local


class LocalAdapterTestCase(unittest.TestCase):

    def setUp(self):
        self.deferred = mock.Mock()
        self.c = mock.MagicMock()

    def test_detach_listener_raises_KeyError_when_route_does_not_exist(self):
        l = Local()
        self.assertRaises(KeyError, partial(l.detach_listener, 'foo'))

    def test_send_raises_KeyError_when_route_has_no_handler(self):
        l = Local()
        self.assertRaises(KeyError, partial(l.send, 'foo', '', None))

    def test_send_calls_attached_callback(self):
        self.c.return_value = self.deferred
        l = Local()
        l.attach_listener('foo', self.c)
        l.send('foo', 'asd', self.deferred)

        self.c.assert_called_once_with('asd')
        self.deferred.then.assert_called_once_with(IsCallable(), IsCallable())

    def test_attach_listener_overrides_handlers(self):
        c_not_called = mock.MagicMock()
        self.c.return_value = self.deferred

        l = Local()
        l.attach_listener('foo', c_not_called)
        l.attach_listener('foo', self.c)
        l.send('foo', 'asd', self.deferred)

        self.c.assert_called_once_with('asd')
        self.assertEqual(c_not_called.call_count, 0)

    def test_send_expects_deferred(self):
        def se(done, fail):
            done('asd')
        self.c.return_value = self.deferred
        self.deferred.then.side_effect=se
        d = mock.Mock()

        l = Local()
        l.attach_listener('foo', self.c)
        l.send('foo', 'asd', d)
        d.resolve.assert_called_once_with(IsA(str))
        self.c.assert_called_once_with('asd')
        self.deferred.then.assert_called_once_with(IsCallable(), IsCallable())

    def test_implements_all_methods_from_abstract_class(self):
        self.assertTrue(hasattr(Local(), 'serve'))
        self.assertTrue(hasattr(Local(), 'connect'))
        self.assertTrue(hasattr(Local(), 'send'))
        self.assertTrue(hasattr(Local(), 'ack'))
        self.assertTrue(hasattr(Local(), 'attach_listener'))
        self.assertTrue(hasattr(Local(), 'detach_listener'))


if "__main__" == __name__:
    unittest.main()
