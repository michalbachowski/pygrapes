#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2011 Michał Bachowski
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
__author__ = "mib"
__date__ = "$2011-01-22 12:02:41$"

import json
import zmq
from pigeon.queue import QueueError, Adapter
try:
    from pprint import pformat
except:
    def pformat(data):
        return str(data)


class ZmqError(QueueError):
	pass


class UnsupportedSocketTypeError(ZmqError):
    pass


class Zmq(Adapter):

    @classmethod
    def name(cls):
        return 'zeromq'

    def __init__(self, type, route='', host='tcp://127.0.0.1:5672', config={}):
        Adapter.__init__(self)
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
            raise UnsupportedSocketTypeError()
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