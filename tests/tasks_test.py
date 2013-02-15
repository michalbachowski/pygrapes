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
import random
import string

##
# other modules
#
from promise import Promise, Deferred

##
# pygrapes modules
#
from pygrapes.core import Core
from pygrapes.tasks import task, task_group, setup_task_group, serve, \
        remove_task_group
from pygrapes import adapter


class TasksTestCase(unittest.TestCase):

    def setUp(self):
        self.mox = mox.Mox()
        # generate unique group name
        # groups are global (intended) so ensure there is no name conflict
        self.group = ''.join([random.choice(string.letters + string.digits) \
                for i in xrange(0, 20)])
        self.core = self.mox.CreateMockAnything()

    def tearDown(self):
        self.mox.UnsetStubs()
        try:
            remove_task_group(self.group)
        except:
            pass

    def test_setup_task_group_expects_group_name(self):
        self.assertTrue(TypeError, setup_task_group)

    def test_setup_task_group_expects_all_arguments_for_Core_instance(self):
        self.assertRaises(TypeError, partial(setup_task_group, self.group))
        setup_task_group(self.group, adapter.Abstract())

    def test_setup_task_group_returns_callable(self):
        self.assertTrue(callable(setup_task_group(self.group, \
                adapter.Abstract())))

    def test_task_group_expects_1_arg(self):
        self.assertRaises(TypeError, task_group)
    
    def test_task_group_allows_2_args(self):
        self.assertRaises(RuntimeError, partial(task_group, None))
    
    def task_group_expects_core_object_for_new_groups(self):
        self.assertRaises(RuntimeError, partial(task_group, self.group, None))

    def test_task_group_disallows_group_reinitialization(self):
        task_group(self.group, self.core)
        self.assertRaises(RuntimeError, partial(task_group, self.group, \
                self.core))

    def test_task_group_allows_using_initialized_groups(self):
        task_group(self.group, self.core)
        task_group(self.group)

    def test_task_returns_callable(self):
        self.assertTrue(callable(task(self.group)))

    def test_task_returns_callable_that_expects_group_to_be_set(self):
        self.assertRaises(KeyError, partial(task(self.group), None))

    def test_callable_returned_by_task_expects_input_with_name_attribute(self):
        task_group(self.group, self.core)
        self.core.add_command(mox.IsA(str), mox.IsA(object))
        self.assertRaises(AttributeError, partial(task(self.group), None))
        self.assertRaises(AttributeError, partial(task(self.group), ''))
        partial(task(self.group), object)()

    def test_callable_returned_by_task_returns_callable(self):
        task_group(self.group, self.core)
        self.core.add_command(mox.IsA(str), mox.IsA(object))
        self.assertTrue(callable(task(self.group)(object)))
        
    def test_task_returns_decorator(self):
        self.core.add_command(mox.IsA(str), mox.IsA(object))
        self.mox.ReplayAll()

        # group must be set up
        task_group(self.group, self.core)
        @task(self.group)
        def foo():
            pass

        self.mox.VerifyAll()

    def test_calls_to_wrapped_functions_are_forwarded_to_core_instance(self):
        self.core.add_command(mox.IsA(str), mox.IsA(object))
        self.core.call(mox.IsA(str), 1, 2, 3).AndReturn('bar')
        self.mox.ReplayAll()

        # group must be set up
        t = task_group(self.group, self.core)

        @t
        def func(a, b, c):
            pass

        self.assertEquals(func(1, 2, 3), 'bar')

        self.mox.VerifyAll()

    def test_remove_task_group_expects_one_arg(self):
        self.assertRaises(TypeError, remove_task_group)

    def test_remove_task_group_removes_predefined_groups(self):
        task_group(self.group, 'a')
        remove_task_group(self.group)
        task_group(self.group, 'a')

    def test_remove_task_group_raises_key_error_when_group_not_exist(self):
        self.assertRaises(KeyError, partial(remove_task_group, self.group))

    def test_serve_expects_no_arguments(self):
        serve()

    def test_serve_allows_to_pass_one_arg(self):
        serve('foo')

    def test_serve_calls_on_each_task_group_core_serve_method(self):
        self.core.serve()
        self.mox.ReplayAll()

        task_group(self.group, self.core)
        serve()

        self.mox.VerifyAll()

    def test_serve_calls_on_given_task_group_core_serve_method(self):
        c = self.mox.CreateMockAnything()
        self.core.serve()
        self.mox.ReplayAll()

        task_group(self.group, self.core)
        task_group('foo', c)
        serve(self.group)

        self.mox.VerifyAll()
        remove_task_group('foo')


if "__main__" == __name__:
    unittest.main()
