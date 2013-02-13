#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Helper function for easy task handling (defining/calling)
"""
from functools import partial, wraps, update_wrapper
from pygrapes.core import Core


__all__ = ['task', 'task_group']


_groups = {}


def remove_task_group(group_name):
    """
    Removed task group configuration
    """
    del _groups[group_name]

def serve(group_name=None):
    """
    Starts server for given group
    """
    [_groups[g].serve() for g in _groups \
            if g == group_name or group_name is None]

def task_group(group_name, core=None):
    """
    Initializes task group.
    Returns function that should be used to decorate command handlers
    """
    if core is not None:
        if group_name in _groups:
            raise RuntimeError('Couldn`t reinitialize task group')
        _groups[group_name] = core
    elif group_name not in _groups:
        raise RuntimeError('Couldn`t use uninitialized group')
    return task(group_name)

def task(group_name):
    """
    Wraps handler function in convinient wrapper
    """
    return partial(_func_decorator, group_name)

def _func_decorator(group_name, function):
    """
    Real decorator function.
    Registers new command in group 'Core' instance.
    """
    _groups[group_name].add_command(function.__name__, function)
    return update_wrapper(partial(_func_wrapper, group_name, \
            function.__name__), function)

def _func_wrapper(group_name, command, *args, **kwargs):
    """
    Real wrapper function.
    Proxies calls to wrapped function to proper 'Core' instance
    """
    return _groups[group_name].call(command, *args, **kwargs)
