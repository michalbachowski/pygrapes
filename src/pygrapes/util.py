#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module with miscellaneous utilities
"""
from functools import partial
import importlib


def _not_implemented(err, *args, **kwargs):
    raise NotImplementedError(err)

def not_implemented(err):
    return partial(_not_implemented, err)
    

def import_object(path):
    """
    Imports class given as complete path, eg: foo.bar.baz.ClassName
    """
    tmp = path.split('.')
    module = '.'.join(tmp[0:-1])
    cls = tmp[-1]
    return getattr(importlib.import_module(module), cls)
