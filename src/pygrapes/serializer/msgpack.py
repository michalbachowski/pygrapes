#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MsgPack serializer
"""
import importlib
from pygrapes.serializer.abstract import Abstract
from pygrapes.util import not_implemented

# discover parser
try:
    t = importlib.import_module('msgpack')
    _decode = getattr(t, 'loads')
    _encode = getattr(t, 'dumps')
except ImportError:
    _decode = _encode = not_implemented('A MsgPack module is required!')


class MsgPack(Abstract):
    """
    Msgpack serializer
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
