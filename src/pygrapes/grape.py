#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Helper function for easy task handling (defining/calling)
"""
from functools import partial, wraps, update_wrapper
from pygrapes.util import import_object
from pygrapes.core import Core


__all__ = ['Grape']


_groups = {}


def remove_task_group(group_name):
    """
    Removed task group configuration
    """
    del _groups[group_name]


def serve(group_name=None):
    """
    Starts server for given group (or all groups)
    """
    [_groups[g].serve() for g in _groups \
            if g == group_name or group_name is None]


class Grape(object):
    """
    PyGrapes working class. Sets up groups and defines wrappers and decorators
    """

    def __init__(self, group_name, core=None, adapter=None, \
            serializer='pygrapes.serializer.Json'):
        """
        Class initialization
        """
        self._group = group_name
        self._setup(core, adapter, serializer)
        self.sync = self.task

    def _setup(self, core, adapter, serializer):
        """
        Sets up task group from given arguments
        """
        if core is not None:
            self._set_task_group(core)
            return
        if isinstance(adapter, str):
            adapter = import_object(adapter)()
        if adapter is None:
            return
        if isinstance(serializer, str):
            serializer = import_object(serializer)()
        if serializer is None:
            return
        self._set_task_group(Core(*args, **kwargs))

    def _set_task_group(self, core=None):
        """
        Initializes task group.
        """
        if core is not None:
            if self._group in _groups:
                raise RuntimeError('Couldn`t reinitialize task group')
            _groups[self._group] = core
        elif self._group not in _groups:
            raise RuntimeError('Couldn`t use uninitialized group')

    def _wrap(self, function):
        """
        Returns wrapper for given function
        """
        return update_wrapper(partial(self._func_wrapper, \
                function.__name__), function)

    def async(self, function):
        """
        Decorator for asynchronous function
        (the one that handles deferred object manually)
        Registers new command in group`s 'Core' instance.
        """
        _groups[self._group].add_command(function.__name__, function)
        return self._wrap(function)

    def _func_wrapper(self, command, *args, **kwargs):
        """
        Real wrapper function.
        Proxies calls to wrapped function to proper 'Core' instance
        """
        return _groups[self._group].call(command, args, kwargs)

    def task(self, function):
        """
        Decorator for synchronous function
        (the one that have deferred object handled automatically)
        Registers new command in group`s 'Core' instance.
        """
        _groups[self._group].add_command(function.__name__, \
                partial(self._sync_call, function))
        return self._wrap(function)
    
    def _sync_call(self, function, *args, **kwargs):
        """
        Synchronous call. Handles 'deferred' object for wrapped function
        """
        deferred = kwargs['deferred']
        del kwargs['deferred']
        try:
            r = function(*args, **kwargs)
        except e:
            deferred.reject({'exception': e})
        else:
            deferred.resolve(r)
