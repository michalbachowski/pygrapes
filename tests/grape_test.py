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
import sys
import unittest
import random
import string

##
# other modules
#
from promise import Promise, Deferred

##
# pygrapes modules
#
from mock_helper import *
from pygrapes.core import Core
from pygrapes.grape import Grape, serve, remove_task_group
from pygrapes import adapter
from pygrapes import serializer


class GrapeTestCase(unittest.TestCase):

    def setUp(self):
        # generate unique group name
        # groups are global (intended) so ensure there is no name conflict
        self.group = ''.join([random.choice(string.letters + string.digits) \
                for i in xrange(0, 20)])
        self.core = mock.Mock()

    def tearDown(self):
        try:
            remove_task_group(self.group)
        except:
            pass

    def test_init_expects_group_name_only(self):
        self.assertTrue(TypeError, Grape)

    def test_init_allows_core_argument(self):
        Grape(self.group, core=None)

    def test_init_allows_adapter_argument(self):
        Grape(self.group, adapter=None)

    def test_init_allows_serializer_argument(self):
        Grape(self.group, serializer=None)

    def test_init_allows_serializer_to_be_passed_as_string(self):
        Grape(self.group, serializer='pygrapes.serializer.Abstract')

    def test_init_expects_valid_abstract_before_serializer_is_loaded(self):
        Grape(self.group, serializer='pygrapes.foo.Bar')

    def test_init_expects_serializer_string_to_be_valid(self):
        self.assertRaises(ImportError, partial(Grape, self.group, \
                adapter=adapter.Abstract(), serializer='pygrapes.foo.Bar'))

    def test_init_expects_serializer_string_to_be_not_None(self):
        self.assertRaises(KeyError, partial(Grape(self.group,
                adapter=adapter.Abstract(), serializer=None).task, object))

    def test_init_allows_adapter_to_be_passed_as_string(self):
        Grape(self.group, adapter='pygrapes.adapter.Abstract')

    def test_init_expects_adapter_string_to_be_valid(self):
        self.assertRaises(ImportError, partial(Grape, self.group, \
                adapter='pygrapes.foo.Bar'))

    def test_init_omit_group_serialization_if_all_arguments_are_None(self):
        self.assertRaises(KeyError, partial(Grape(self.group, core=None, \
                adapter=None, serializer=None).task, object))

    def test_init_disallows_group_reinitialization(self):
        Grape(self.group, self.core)
        self.assertRaises(RuntimeError, partial(Grape, self.group, \
                self.core))

    def test_init_allows_using_initialized_groups(self):
        Grape(self.group, self.core)
        Grape(self.group)

    def test_task_expects_argument(self):
        self.assertRaises(TypeError, Grape(self.group).task)

    def test_task_expects_group_to_be_properly_initialized(self):
        self.assertRaises(KeyError, partial(Grape(self.group).task, object))

    def test_callable_returned_by_task_expects_input_with_name_attribute(self):
        g = Grape(self.group, self.core)
        self.assertRaises(AttributeError, partial(g.task, None))
        self.assertRaises(AttributeError, partial(g.task, ''))
        g.task(object)
        self.core.add_command.assert_called_once_with(IsA(str), IsCallable())

    def test_callable_returned_by_task_returns_callable(self):
        g = Grape(self.group, self.core)
        self.assertTrue(callable(g.task(object)))
        self.core.add_command.assert_called_once_with(IsA(str), IsCallable())

    def test_task_returns_decorator(self):
        # group must be set up
        g = Grape(self.group, self.core)
        @g.task
        def foo():
            pass
        self.core.add_command.assert_called_once_with(IsA(str), IsCallable())

    def test_calls_to_wrapped_functions_are_forwarded_to_core_instance(self):
        self.core.call = mock.MagicMock(return_value='bar')
        # group must be set up
        g = Grape(self.group, self.core)

        @g.task
        def func(a, b, c):
            pass

        self.assertEquals(func(1, 2, 3), 'bar')
        self.core.add_command.assert_called_once_with(IsA(str), IsCallable())
        self.core.call.assert_called_once_with(IsA(str), (1, 2, 3), {})

    def test_task_allows_wrapped_functions_to_omit_deferred_input(self):
        callback = mock.MagicMock()

        # using existing implementations - didn`t want to implement them here
        c = Core(adapter.Local(), serializer.Json())

        g = Grape(self.group, c)
        # decorate method foo
        @g.task
        def foo(a,b,c):
            return a+b+c
        # call foo
        p = foo(1,2,3).done(callback)

        # verify promise state
        self.assertTrue(p.resolved)
        callback.assert_called_once_with(6)

    def test_task_takes_care_of_exceptions(self):
        callback = mock.MagicMock()
        # using existing implementations - didn`t want to implement them here
        c = Core(adapter.Local(), serializer.Json())

        g = Grape(self.group, c)
        # decorate method foo
        @g.task
        def foo(a,b,c):
            raise RuntimeError('bar')
        # call foo
        p = foo(1,2,3).fail(callback).done(callback)

        # verify promise state
        self.assertFalse(p.resolved)
        self.assertTrue(p.rejected)
        callback.assert_called_once_with(exception=IsA(dict))

    def test_async_expects_argument(self):
        self.assertRaises(TypeError, Grape(self.group).async)

    def test_async_expects_group_to_be_initialized(self):
        self.assertRaises(KeyError, partial(Grape(self.group).async, object))

    def test_async_returns_callable(self):
        self.assertTrue(callable(Grape(self.group, core=self.core).async(\
                object)))

    def test_callable_returned_by_async_expects_additional_input(self):
        g = Grape(self.group, self.core)
        self.assertRaises(AttributeError, partial(g.async, None))
        self.assertRaises(AttributeError, partial(g.async, ''))
        g.async(object)
        self.core.add_command.assert_called_once_with(IsA(str), IsCallable())

    def test_callable_returned_by_async_returns_callable(self):
        g = Grape(self.group, self.core)
        self.assertTrue(callable(g.async(object)))
        self.core.add_command.assert_called_once_with(IsA(str), IsCallable())

    def test_async_returns_decorator(self):
        # group must be set up
        g = Grape(self.group, self.core)
        @g.async
        def foo():
            pass
        self.core.add_command.assert_called_once_with(IsA(str), IsCallable())

    def test_async_forces_wrapped_functions_to_expect_deferred_named_arg(self):
        callback = mock.MagicMock()
        # using existing implementations - didn`t want to implement them here
        c = Core(adapter.Local(), serializer.Json())

        g = Grape(self.group, c)
        # decorate method foo
        @g.async
        def foo(a,b,c, deferred):
            deferred.resolve(a+b+c)
        # call foo
        p = foo(1,2,3).done(callback)

        # verify promise state
        self.assertTrue(p.resolved)
        callback.assert_called_once_with(6)

    def test_async_expects_wrapped_functions_to_manually_handle_deferred(self):
        callback = mock.MagicMock()
        # using existing implementations - didn`t want to implement them here
        c = Core(adapter.Local(), serializer.Json())

        g = Grape(self.group, c)
        # decorate method foo
        @g.async
        def foo(a,b,c, deferred):
            return a+b+c
        # call foo
        p = foo(1,2,3).done(callback)

        # verify promise state
        self.assertFalse(p.resolved)
        self.assertFalse(p.rejected)
        self.assertFalse(p.cancelled)
        self.assertEqual(callback.call_count, 0)

    def test_remove_task_group_expects_one_arg(self):
        self.assertRaises(TypeError, remove_task_group)

    def test_remove_task_group_removes_predefined_groups(self):
        Grape(self.group, 'a')
        remove_task_group(self.group)
        Grape(self.group, 'a')

    def test_remove_task_group_raises_key_error_when_group_not_exist(self):
        self.assertRaises(KeyError, partial(remove_task_group, self.group))

    def test_serve_expects_no_arguments(self):
        serve()

    def test_serve_allows_to_pass_one_arg(self):
        serve('foo')

    def test_serve_calls_on_each_task_group_core_serve_method(self):
        Grape(self.group, self.core)
        serve()
        self.core.serve.assert_called_once_with()

    def test_serve_calls_on_given_task_group_core_serve_method(self):
        c = mock.MagicMock()

        g = Grape(self.group, self.core)
        g = Grape('foo', c)
        serve(self.group)

        self.core.serve.assert_called_once_with()
        self.assertEqual(c.call_count, 0)
        self.assertEqual(c.serve.call_count, 0)
        remove_task_group('foo')

    def test_format_exception_expects_1_arg(self):
        self.assertRaises(TypeError, Grape(self.group).format_exception)

    def test_format_exception_allows_2_args(self):
        self.assertRaises(AttributeError, \
                partial(Grape(self.group).format_exception, None, None))

    def test_format_exception_expects_exception_as_input(self):
        e = mock.MagicMock()
        e.message = 'foo'
        e.args = 'bar'
        
        fe = Grape(self.group).format_exception(e)
        self.assertEquals(fe['args'], e.args)
        self.assertTrue(isinstance(fe['traceback'], list))

    def test_format_exception_allows_to_pass_traceback(self):
        e = mock.MagicMock()
        e.message = 'foo'
        e.args = 'bar'
        # prepare valid traceback
        try:
            raise RuntimeError('a')
        except:
            pass
        exc_type, exc_value, exc_traceback = sys.exc_info()

        fe = Grape(self.group).format_exception(e, exc_traceback)
        self.assertEquals(fe['args'], e.args)
        self.assertTrue(isinstance(fe['traceback'], list))
        self.assertTrue(len(fe['traceback'])>0)

    def test_format_exception_expects_traceback_to_be_valid(self):
        e = mock.MagicMock()
        e.message = 'foo'
        e.args = 'bar'

        self.assertRaises(AttributeError, partial(
                Grape(self.group).format_exception, e, 'f'))


if "__main__" == __name__:
    unittest.main()
