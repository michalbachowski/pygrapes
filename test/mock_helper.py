#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections


__all__ = ['IsA', 'IsCallable', 'results']


class IsA(object):

    def __init__(self, cls):
        self.cls = cls

    def __eq__(self, other):
        return isinstance(other, self.cls)


class IsCallable(IsA):

    def __init__(self):
        self.cls = collections.Callable


def results(*args):
    results = list(args)
    def looper(*args):
        r = results.pop(0)
        if isinstance(r, BaseException):
            raise r
        return r
    return looper
