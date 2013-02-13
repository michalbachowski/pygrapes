#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Core class for PyGrapes framework.

It is responsible for message preperation and passing
"""
from functools import partial
from promise import Deferred


__all__ = ['Core']


class Core(object):
    """
    Core class for PyGrapes framework.

    It is responsible for message preperation and passing
    """

    def __init__(self, adapter, serializer=None):
        """
        Object initialization
        """
        self._adapter = adapter
        self._serializer = serializer

    def serve(self):
        """
        Starts core in "server" mode
        """
        pass

    def call(self, command, args=None, kwargs=None):
        """
        Calls given command with given attributes.
        Function should be given as a string.
        """
        return Deferred(partial(self._adapter.send, str(command), \
                self._prepare_msg(args, kwargs))).promise()

    def _prepare_msg(self, args, kwargs):
        """
        Preapres message structure for given arguments
        """
        return self._serializer.dumps({'args': args or [], \
                'kwargs': kwargs or {}})

    def _parse_msg(self, message):
        """
        Parses message string to local structure
        """
        return self._serializer.loads(message)

    def _wrapper(self, callback, message, deferred):
        """
        Calls given command with given data
        """
        tmp = self._parse_msg(message)
        tmp['kwargs']['deferred'] = deferred
        callback(*tmp['args'], **tmp['kwargs'])

    def add_command(self, command, callback):
        """
        Attaches given callback to handle calls to given command
        """
        self._adapter.attach_listener(str(command), partial(self._wrapper, \
                callback))
        return self

    def del_command(self, command):
        """
        Removes given command
        """
        self._adapter.detach_listener(str(command))
        return self
