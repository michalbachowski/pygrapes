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
# other modules
#
from promise import Promise, Deferred

##
# pygrapes modules
#
from pygrapes  import Core, adapter, serializer


class CoreTestCase(unittest.TestCase):

    def setUp(self):
        self.mox = mox.Mox()
        self.adapter = self.mox.CreateMock(adapter.Abstract)
        self.serializer = self.mox.CreateMock(serializer.Abstract)
        self.core = Core(self.adapter, self.serializer)

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_init_expects_adapter(self):
        self.assertRaises(TypeError, Core)

    def test_init_allows_passing_serializer(self):
        Core(None, None)

    def test_serve_expects_no_arguments(self):
        self.assertRaises(AttributeError, Core(None, None).serve)

    def test_serve_calls_adapter_serve(self):
        self.adapter.serve()
        self.mox.ReplayAll()

        self.core.serve()

        self.mox.VerifyAll()

    def test_serve_cannot_be_called_after_connect(self):
        self.core.connect()
        self.assertRaises(RuntimeError, self.core.serve)
    
    def test_serve_called_sequentially_does_nothing(self):
        self.adapter.serve()
        self.mox.ReplayAll()
        
        self.core.serve()
        self.core.serve()

        self.mox.VerifyAll()

    def test_connect_expects_no_arguments(self):
        self.assertRaises(AttributeError, Core(None, None).connect)

    def test_connect_calls_adapter_connect(self):
        self.adapter.connect()
        self.mox.ReplayAll()

        self.core.connect()

        self.mox.VerifyAll()

    def test_connect_cannot_be_called_after_serve(self):
        self.core.serve()
        self.assertRaises(RuntimeError, self.core.connect)

    def test_connect_called_sequentially_does_nothing(self):
        self.adapter.connect()
        self.mox.ReplayAll()

        self.core.connect()
        self.core.connect()
        
        self.mox.VerifyAll()

    def test_call_expects_function_name(self):
        self.adapter.connect()
        self.adapter.send(mox.IsA(str), mox.IsA(str), \
                deferred=mox.IsA(Deferred)).AndReturn(Deferred())
        self.serializer.dumps(mox.IsA(dict)).AndReturn('')
        self.mox.ReplayAll()
        self.assertRaises(TypeError, self.core.call)
        self.assertTrue(self.core.call('a') is not None)
        self.mox.VerifyAll()

    def test_call_expects_one_serializable_rgument_1(self):
        class Foo(object):
            pass

        self.adapter.connect()
        for i in xrange(0, 4):
            self.serializer.dumps(mox.IsA(dict)).AndReturn('')
            self.adapter.send(mox.IsA(str), mox.IsA(str), \
                    deferred=mox.IsA(Deferred)).AndReturn(Deferred())

        self.mox.ReplayAll()
        self.assertFalse(self.core.call('abc') is None)
        self.assertFalse(self.core.call('abc', [1,2,3]) is None)
        self.assertFalse(self.core.call('abc', kwargs={'a': 1}) is None)
        self.assertFalse(self.core.call('abc', [1,2,3], {'a': 1, \
                'b': [1,2,3], 'c': {'g': 3}}) is None)
        self.mox.VerifyAll()

    def test_call_returns_promise(self):
        self.adapter.connect()
        self.adapter.send(mox.IsA(str), mox.IsA(str), \
                deferred=mox.IsA(Deferred)).AndReturn(Deferred())
        self.serializer.dumps(mox.IsA(dict)).AndReturn('')
        self.mox.ReplayAll()
        self.assertTrue(isinstance(self.core.call(''), Promise))
        self.mox.VerifyAll()

    def test_add_command_required_2_args(self):
        self.assertRaises(TypeError, self.core.add_command)
        self.assertRaises(TypeError, partial(self.core.add_command, None))
        self.assertFalse(self.core.add_command(None, None) is None)

    def test_add_command_returns_instance_of_Core(self):
        self.assertTrue(isinstance(self.core.add_command(None, None), Core))
    
    def test_del_command_required_1_arg(self):
        self.assertRaises(TypeError, self.core.add_command)
        self.core.add_command(None, None)
        self.assertFalse(self.core.del_command(None) is None)

    def test_del_command_returns_instance_of_Core(self):
        self.core.add_command(None, None)
        self.assertTrue(isinstance(self.core.del_command(None), Core))

    def test_del_command_does_not_require_command_to_be_added(self):
        self.core.del_command(None)

    def test_add_command_calls_adapter(self):
        self.adapter.attach_listener(mox.IsA(str), mox.IsA(object))
        self.mox.ReplayAll()

        self.core.add_command(None, None)

        self.mox.VerifyAll()

    def test_del_command_calls_adapter(self):
        self.adapter.attach_listener(mox.IsA(str), mox.IsA(object))
        self.adapter.detach_listener(mox.IsA(str))
        self.mox.ReplayAll()

        self.core.add_command(None, None)
        self.core.del_command(None)

        self.mox.VerifyAll()

    def test_callbacks_are_called_with_all_input_arguments(self):
        callbacks = {}
        def al(route, cb):
            callbacks[route] = cb

        def snd(route, message, deferred):
            callbacks[route](message)

        # serialization
        obj = {'args': [1, 'a'], 'kwargs': {'c': 'foo', 'd': [1,2,3]}}
        rep = '{"args": [1, "a"], "kwargs": {"c": "foo", "d": [1,2,3]}}'
        # adapter
        self.adapter.attach_listener(mox.IsA(str), mox.IsA(partial))\
                .WithSideEffects(al)
        self.serializer.dumps(mox.IsA(dict)).AndReturn(rep)
        self.adapter.connect()
        self.adapter.send(mox.IsA(str), rep, deferred=mox.IsA(Deferred))\
                .WithSideEffects(snd)
        # callback
        c = self.mox.CreateMockAnything()
        c(1, 'a', c='foo', d=[1,2,3], deferred=mox.IsA(Deferred))
        self.serializer.loads(rep).AndReturn(obj)
        
        # test
        self.mox.ReplayAll()

        self.core.add_command('foo', c)
        self.core.call('foo', [1, 'a'], {'c': 'foo', 'd': [1,2,3]})

        self.mox.VerifyAll()


if "__main__" == __name__:
    unittest.main()
