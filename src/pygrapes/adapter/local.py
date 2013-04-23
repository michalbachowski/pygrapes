#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PyGrapes adapter that allows call local methods.
Thatks to this in future one can migrate to any other adapter 
without modifiying internal app code.
"""
from pygrapes.adapter import Abstract


class Local(Abstract):
    """
    Local procedure call adapter
    """

    def send(self, route, message, deferred):
        """
        Sends message to given route. Accepts 'deferred' keyword argument.
        """
        self._listeners[route](message).then(deferred.resolve, deferred.reject)
