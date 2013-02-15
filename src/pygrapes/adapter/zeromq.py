#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Adapters for ZeroMQ backend
"""
import zmq
from pygrapes.adapter.abstract import Abstract


class Zmq(Abstract):
    """
    Adapter for vanilla ZeroMQ client library (pyzmq)
    """
    
    def __init__(self, type, route='', host='tcp://127.0.0.1:5672', config={}):
        self.types = {\
            'pubsub': {\
                'publish': zmq.PUB,\
                'consume': zmq.SUB},\
            'reqrep': {\
                'publish': zmq.REQ,\
                'consume': zmq.REP},\
            'xreqxrep': {\
                'publish': zmq.XREQ,\
                'consume': zmq.XREP},\
            'pullpush': {\
                'publish': zmq.PUSH,\
                'consume': zmq.PULL},\
        }
        if type not in self.types:
            raise KeyError('Unsupported type')
        self.type = type
        self.route = route
        self.host = host
        self.config = config

        self.context = None
        self.socket = None

    def _init(self, mode):
        if self.socket is not None:
            return
        self.log.debug('Starting ZMQ adapter: type=%s; mode=%s; route=%s, host=%s; config: %s',\
            self.type, mode, self.route, self.host, pformat(self.config))
        # context
        self.context = zmq.Context()
        # socket
        self.socket = self.context.socket(self.types[self.type][mode])
        if 'consume' == mode:
            self.socket.connect(self.host)
        else:
            self.socket.bind(self.host)

        for (opt, val) in self.config.iteritems():
            self.socket.setsockopt(opt, val)
        if 'consume' == mode and 'pubsub' == self.type:
            self.socket.setsockopt(zmq.SUBSCRIBE, self.route)

    def send(self, route, message, deferred):
        """
        Sends message to given route. Accepts 'deferred' keyword argument.
        """
        pass

    def attach_listener(self, route, callback):
        """
        Binds callback with message with given route.
        When message with given route was received given callback is called
        with 'deferred' keyword argument that is used to pass back response.
        """
        pass
    
    def detach_listener(self, route):
        """
        Unbinds callback from message with given route.
        """
        pass

    def consume(self, callback):
        self._init('consume')
        func = self.on_new_message(callback)
        try:
            while True:
                # route key
                self.socket.recv()
                # message itself
                func(self.socket.recv())
        except KeyboardInterrupt:
            raise

    def on_new_message(self, callback):
        def callback_func(message):
            self.log.debug(message)
            body = json.loads(message)
            try:
                callback(body)
            except:
                self.log.exception('An exception occurred in consumer callback')
        return callback_func

    def publish(self,message):
        self._init('publish')
        msg = json.dumps(message)

        self.log.info("Sending message with route '%s'" % self.route)
        self.log.debug(msg)
        self.socket.send(self.route, zmq.SNDMORE)
        self.socket.send(msg)
