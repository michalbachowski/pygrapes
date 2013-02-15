#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
JSON serializer
"""
from pygrapes.serializer import Abstract
import importlib

# discover JSON parser
_implementations = [('json', 'loads', 'dumps'), ('cjson', 'decode', 'encode'), \
    ('simplejson', 'loads', 'dumps'), ('django.utils.simplejson', 'loads', \
    'dumps')]

def _encode(s):
    raise NotImplementedError('A JSON parser is required!')

_decode = _encode

for (module, loads, dumps) in _implementations:
    try:
        t = importlib.import_module(module)
        _decode = getattr(t, loads)
        _encode = getattr(t, dumps)
        break
    except ImportError:
        pass


class Json(Abstract):
    """
    JSON serializer
    """

    def loads(self, data):
        """
        Method converts given string to internal objects
        """
        return _decode(data)

    def dumps(self, data):
        """
        Method converts given internal objects to string
        """
        return _encode(data)
