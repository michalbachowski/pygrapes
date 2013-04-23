#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Abstract class for all serializers
"""


class Abstract(object):
    """
    Abstract class for all serializers
    """

    def loads(self, data):
        """
        Method converts given string to internal objects
        """
        raise NotImplementedError()

    def dumps(self, data):
        """
        Method converts given internal objects to string
        """
        raise NotImplementedError()
