#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module with miscellaneous utilities
"""
from functools import partial


def _not_implemented(err, *args, **kwargs):
    raise NotImplementedError(err)

def not_implemented(err):
    return partial(_not_implemented, err)
