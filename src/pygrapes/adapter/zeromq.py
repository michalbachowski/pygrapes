#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Adapters for ZeroMQ backend
"""
import zmq
from pygrapes.adapter import Abstract


class Zmq(Abstract):
    """
    Adapter for vanilla ZeroMQ client library (pyzmq)
    """

    def __init__(self, host='tcp://127.0.0.1:5672', config=None, context=None):
        self._host = host
        self._config = config or {}

        self._context = context or zmq.Context()
        self._socket = None
        Abstract.__init__(self)

    def serve(self):
        """
        Starts adapter in serving mode
        """
        if self._socket is not None:
            return
        self._socket = self._context.socket(zmq.REP)
        self._socket.bind(self._host)

        try:
            while True:
                route = self._socket.recv()
                message = self._socket.recv()
                self._listeners[route](message).done(self._socket.send)
        except KeyboardInterrupt:
            raise

    def connect(self):
        """
        Starts adapter in client mode
        """
        if self._socket is not None:
            return self
        self._socket = self._context.socket(zmq.REQ)
        self._socket.connect(self._host)
        self._configure()
        return self

    def _configure(self):
        """
        Sets configuration for socket
        """
        for (opt, val) in self._config.iteritems():
            self._socket.setsockopt(opt, val)

    def send(self, route, message, deferred):
        """
        Sends message to given route. Accepts 'deferred' keyword argument.
        """
        self._socket.send(route, zmq.SNDMORE)
        self._socket.send(message)
        return deferred.resolve(self._socket.recv())
