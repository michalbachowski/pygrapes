#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# hack for loading modules
#
from _path import fix, mock
fix()

##
# python standard library
#
from functools import partial
import unittest

##
# other modules
#
from promise import Promise, Deferred

##
# pygrapes modules
#
from mock_helper import *
from pygrapes  import Core


class CoreTestCase(unittest.TestCase):

    def setUp(self):
        self.adapter = mock.Mock()
        self.serializer = mock.Mock()
        self.core = Core(self.adapter, self.serializer)

    def test_init_expects_adapter(self):
        self.assertRaises(TypeError, Core)

    def test_init_allows_passing_serializer(self):
        Core(None, None)

    def test_serve_expects_no_arguments(self):
        self.assertRaises(AttributeError, Core(None, None).serve)

    def test_serve_calls_adapter_serve(self):
        self.core.serve()
        self.adapter.serve.assert_called_once_with()

    def test_serve_cannot_be_called_after_connect(self):
        self.adapter.serve() # to be able to verify "assert_called_once"
        self.core.connect()
        self.assertRaises(RuntimeError, self.core.serve)
        self.adapter.serve.assert_called_once_with()
        self.adapter.connect.assert_called_once_with()

    def test_serve_called_sequentially_does_nothing(self):
        self.core.serve()
        self.core.serve()
        self.adapter.serve.assert_called_once_with()

    def test_connect_expects_no_arguments(self):
        self.assertRaises(AttributeError, Core(None, None).connect)

    def test_connect_calls_adapter_connect(self):
        self.core.connect()
        self.adapter.connect.assert_called_once_with()

    def test_connect_cannot_be_called_after_serve(self):
        self.adapter.connect() # to be able to verify "assert_called_once"
        self.core.serve()
        self.assertRaises(RuntimeError, self.core.connect)
        self.adapter.serve.assert_called_once_with()
        self.adapter.connect.assert_called_once_with()

    def test_connect_called_sequentially_does_nothing(self):
        self.core.connect()
        self.core.connect()
        self.adapter.connect.assert_called_once_with()

    def test_call_expects_one_arg(self):
        self.assertRaises(TypeError, self.core.call)

    def test_call_expects_function_name(self):
        self.serializer.dumps = mock.MagicMock(return_value='')
        self.assertTrue(self.core.call('a') is not None)
        self.serializer.dumps.assert_called_once_with({'args': [], \
                'kwargs': {}})
        self.adapter.send.assert_called_once_with('a', '', 
                deferred=IsA(Deferred))

    def test_call_expects_list_of_args_or_dict_of_kwargs(self):
        self.assertFalse(self.core.call('abc') is None)
        self.assertFalse(self.core.call('abc', [1,2,3]) is None)
        self.assertFalse(self.core.call('abc', kwargs={'a': 1}) is None)
        self.assertFalse(self.core.call('abc', [1,2,3], {'a': 1, \
                'b': [1,2,3], 'c': {'g': 3}}) is None)

    def test_call_returns_promise(self):
        self.assertTrue(isinstance(self.core.call(''), Promise))

    def test_add_command_required_2_args(self):
        self.assertRaises(TypeError, self.core.add_command)
        self.assertRaises(TypeError, partial(self.core.add_command, None))

    def test_add_command_returns_instance_of_Core(self):
        self.assertTrue(isinstance(self.core.add_command(None, None), Core))

    def test_add_command_calls_adapter(self):
        self.assertTrue(isinstance(self.core.add_command(None, None), Core))
        self.adapter.attach_listener.assert_called_once_with('None',
                IsA(partial))

    def test_del_command_required_1_arg(self):
        self.assertRaises(TypeError, self.core.add_command)
        self.core.add_command(None, None)
        self.assertFalse(self.core.del_command(None) is None)

    def test_del_command_returns_instance_of_Core(self):
        self.core.add_command(None, None)
        self.assertTrue(isinstance(self.core.del_command(None), Core))

    def test_del_command_depends_on_adapter_in_case_of_finding_route(self):
        self.core.del_command(None)
        self.adapter.detach_listener = mock.MagicMock(side_effect=KeyError)
        self.assertRaises(KeyError, partial(self.core.del_command, None))

    def test_del_command_calls_adapter(self):
        self.core.del_command(None)
        self.adapter.detach_listener.assert_called_once_with('None')

    def test_callbacks_are_called_with_all_input_arguments(self):
        """

        # serialization
        obj = {'args': [1, 'a'], 'kwargs': {'c': 'foo', 'd': [1,2,3]}}
        rep = '{"args": [1, "a"], "kwargs": {"c": "foo", "d": [1,2,3]}}'
        # adapter
        self._adapter.attach_listener(mox.IsA(str), mox.IsA(partial))\
                .WithSideEffects(al)
        self._serializer.dumps(mox.IsA(dict)).AndReturn(rep)
        self._adapter.connect()
        self._adapter.send(mox.IsA(str), rep, deferred=mox.IsA(Deferred))\
                .WithSideEffects(snd)
        # callback
        c = self.mox.CreateMockAnything()
        c(1, 'a', c='foo', d=[1,2,3], deferred=mox.IsA(Deferred))
        self._serializer.loads(rep).AndReturn(obj)

        # test
        self.mox.ReplayAll()

        self._core.add_command('foo', c)
        self._core.call('foo', [1, 'a'], {'c': 'foo', 'd': [1,2,3]})

        self.mox.VerifyAll()
        """
        # adapter
        callbacks = {}
        def attach(route, cb):
            callbacks[route] = cb

        def send(route, message, deferred):
            callbacks[route](message)
        self.adapter.attach_listener = mock.MagicMock(side_effect=attach)
        self.adapter.send = mock.MagicMock(side_effect=send)

        # serializer
        vrs = {'args': [1, 'a'], 'kwargs': {'c': 'foo', 'd': [1,2,3]}}
        self.serializer.dumps = mock.MagicMock(return_value='dumps')
        self.serializer.loads = mock.MagicMock(return_value=vrs)
        # callback
        c = mock.MagicMock()

        # call
        self.core.add_command('foo', c).call('foo', vrs['args'], vrs['kwargs'])

        # verify
        c.assert_called_once_with(*vrs['args'], deferred=IsA(Deferred),
                **vrs['kwargs'])


if "__main__" == __name__:
    unittest.main()
