#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Helper function for easy task handling (defining/calling)
"""
from functools import partial, wraps, update_wrapper
import importlib
from pygrapes.core import Core
from pygrapes.tasks import sync_task, task, task_group, setup_task_group, serve


__all__ = ['Grape']


class Grape(object):

    def __init__(self, group_name, core=None, adapter=None, \
            serializer='pygrapes.serializer.Json'):
        """
        Class initialization
        """
        self._setup(group_name, core, adapter, serializer)
        self.task = self.sync = self.synchronous = sync_task(group_name)
        self.async = self.asynchronous = task(group_name)

    def _setup(self, group_name, core, adapter, serializer):
        if core is not None:
            task_group(group_name, core)
            return
        if isinstance(adapter, str):
            adapter = self._import(adapter)
        if isinstance(serializer, str):
            serializer = self._import(serializer)
        setup_task_group(group_name, adapter, serializer)

    def _import(self, path):
        """
        """
        tmp = path.split('.')
        module = '.'.join(tmp[0:-1])
        cls = tmp[-1]
        return getattr(importlib.import_module(module), cls)()

