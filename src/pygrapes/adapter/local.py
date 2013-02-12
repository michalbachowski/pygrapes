#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PyGrapes adapter that allows call local methods.
Thatks to this in future one can migrate to any other adapter 
without modifiying internal app code.
"""


class Local(object):
    """
    Local procedure call adapter
    """

    def __init__(self):
        """
        Object initialization
        """
        self._listeners = {}

    def send(self, route, message, deferred):
        """
        Sends message to given route. Accepts 'deferred' keyword argument.
        """
        self._listeners[route](message, deferred=deferred)

    def attach_listener(self, route, callback):
        """
        Binds callback with message with given route.
        When message with given route was received given callback is called
        with 'deferred' keyword argument that is used to pass back response.
        """
        self._listeners[route] = callback
    
    def detach_listener(self, route):
        """
        Unbinds callback from message with given route.
        """
        del self._listeners[route]
