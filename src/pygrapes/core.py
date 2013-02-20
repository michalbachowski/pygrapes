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

    def __init__(self, adapter, serializer):
        """
        Object initialization
        """
        self._adapter = adapter
        self._serializer = serializer
        self._serve = False
        self._connect = False

    def serve(self):
        """
        Starts core in "server" mode
        """
        if self._connect:
            raise RuntimeError('Could not use server mode while in client mode')
        if self._serve:
            return
        self._adapter.serve()
        self._serve = True

    def connect(self):
        """
        Starts core in "client" mode
        """
        if self._serve:
            raise RuntimeError('Could not use client mode while in serve mode')
        if self._connect:
            return
        self._adapter.connect()
        self._connect = True

    def call(self, command, args=None, kwargs=None):
        """
        Calls given command with given attributes.
        Function should be given as a string.
        """
        self.connect()
        d2 = Deferred()

        d1 = Deferred(partial(self._adapter.send, str(command), \
                self._prepare_msg(args, kwargs)))\
            .then(partial(self._unserialize, d2.resolve), 
                    partial(self._unserialize, d2.reject))
        return d2.promise()

    def _unserialize(self, callback, message):
        """
        Unserializes given message and calls given callback
        """
        tmp = self._parse_msg(message)
        callback(*tmp['args'], **tmp['kwargs'])

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

    def _wrapper(self, callback, message):
        """
        Calls given command with given data
        """
        tmp = self._parse_msg(message)
        d2 = Deferred()
        d1 = Deferred(partial(callback, *tmp['args'], **tmp['kwargs']))\
                .then(partial(self._serialize, d2.resolve), 
                        partial(self._serialize, d2.reject))
        return d2.promise()

    def _serialize(self, callback, *args, **kwargs):
        """
        Serializes given arguments and calls callback
        """
        callback(self._prepare_msg(args, kwargs))


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
