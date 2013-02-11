#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Core class for PyGrapes framework.

It is responsible for message preperation and passing
"""
from functools import partial
from promise import Deferred


__all__ = ['Core']


def _command2route(command):
    """
    Prepares route name from given command name
    """
    return '%s$' % command


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
        self._commands = {}

    def call(self, command, args=None, kwargs=None):
        """
        Calls given command with given attributes.
        Function should be given as a string.
        """
        return Deferred(partial(self._adapter.send, _command2route(command), \
                self._prepare_msg(args, kwargs))).promise()

    def _prepare_msg(self, args, kwargs):
        """
        Preapres message structure for given arguments
        """
        return self._serializer.dumps({'args': args or [], \
                'kwargs': kwargs or {}})

    def add_command(self, command, callback):
        """
        Attaches given callback to handle calls to given command
        """
        route = _command2route(command)
        self._commands[route] = callback
        self._adapter.attach_listener(route, callback)
        return self

    def del_command(self, command):
        """
        Removes given command
        """
        self._adapter.detach_listener(_command2route(command))
        del self._commands[_command2route(command)]
        return self
