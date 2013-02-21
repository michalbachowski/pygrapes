#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Base class for all adapters
"""


class Abstract(object):
    """
    Base abstract class for all adapters
    """

    def __init__(self, *args, **kwargs):
        """
        Class initialization
        """
        self._listeners = {}

    def serve(self):
        """
        Starts adapter in serving mode
        """
        pass

    def connect(self):
        """
        Starts adapter in client mode
        """
        pass

    def send(self, route, message, deferred):
        """
        Method to be implemented by all adapters.
        Sends message to given route. Accepts 'deferred' keyword argument.
        """
        raise NotImplementedError()

    def attach_listener(self, route, callback):
        """
        Method to be implemented by all adapters.
        Binds callback with message with given route.
        When message with given route was received given callback is called
        with 'deferred' keyword argument that is used to pass back response.
        """
        self._listeners[route] = callback
        return self
    
    def detach_listener(self, route):
        """
        Method to be implemented by all adapters.
        Unbinds callback from message with given route.
        """
        del self._listeners[route]
        return self

    def ack(self, message):
        """
        Method may be implemented by some adapters.
        Sends information that message was processed.
        """
        pass
