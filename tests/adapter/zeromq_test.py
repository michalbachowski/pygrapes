#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# hack for loading modules
#
import _path
_path.fix()

##
# python standard library
#
from functools import partial
import unittest
import mox

##
# ZeroMQ modules
try:
    import zmq
except ImportError:
    zmq = None

##
# promise modules
from promise import Deferred

##
# pygrapes modules
#
from pygrapes.adapter import Zmq

@unittest.skipIf(zmq is None, 'Missing zmq Python library')
class ZmqAdapterTestCase(unittest.TestCase):

    def setUp(self):
        self.mox = mox.Mox()
        self.ctx = self.mox.CreateMock(zmq.Context)
        self.socket = self.mox.CreateMock(zmq.Socket)
        self.deferred = self.mox.CreateMock(Deferred)

    def setUpConnect(self):
        self.ctx.socket(mox.IsA(int)).AndReturn(self.socket)
        self.socket.connect(mox.IsA(str))

    def setUpBind(self):
        self.ctx.socket(mox.IsA(int)).AndReturn(self.socket)
        self.socket.bind(mox.IsA(str))

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_init_expects_no_args(self):
        self.assertFalse(Zmq() is None)

    def test_init_allows_to_pass_config_arg(self):
        self.assertFalse(Zmq(config={}) is None)

    def test_init_allows_to_pass_context_arg(self):
        self.assertFalse(Zmq(context='foo') is None)

    def test_connects_expects_valid_context_instance(self):
        self.assertRaises(TypeError, Zmq().connect())

    def test_connects_expects_valid_context_instance(self):
        self.setUpConnect()
        self.mox.ReplayAll()

        Zmq(context=self.ctx).connect()

        self.mox.VerifyAll()

    def test_connect_return_instance_of_self(self):
        self.setUpConnect()
        self.mox.ReplayAll()

        self.assertTrue(isinstance(Zmq(context=self.ctx).connect(), Zmq))

        self.mox.VerifyAll()

    def test_connect_will_not_instantinate_socket_twice(self):
        self.setUpConnect()
        self.mox.ReplayAll()

        z = Zmq(context=self.ctx)
        self.assertTrue(isinstance(z.connect(), Zmq))
        self.assertTrue(isinstance(z.connect(), Zmq))

        self.mox.VerifyAll()

    def test_connects_expects_valid_config_instance(self):
        self.setUpConnect()
        self.mox.ReplayAll()

        self.assertRaises(AttributeError,
                Zmq(context=self.ctx, config='a').connect)

        self.mox.VerifyAll()

    def test_connects_expects_valid_config_instance_1(self):
        self.setUpConnect()
        cfg = self.mox.CreateMock(dict)
        cfg.iteritems().AndReturn([])
        self.mox.ReplayAll()

        Zmq(context=self.ctx, config=cfg).connect()

        self.mox.VerifyAll()

    def test_connects_triggers_socket_configuration(self):
        self.setUpConnect()
        cfg = self.mox.CreateMock(dict)
        cfg.iteritems().AndReturn({'a': 1}.iteritems())
        self.socket.setsockopt('a', 1)
        self.mox.ReplayAll()

        Zmq(context=self.ctx, config=cfg).connect()

        self.mox.VerifyAll()


    def test_send_expects_3_args(self):
        z = Zmq()
        self.assertRaises(TypeError, z.send)
        self.assertRaises(TypeError, partial(z.send, None))
        self.assertRaises(TypeError, partial(z.send, None, None))
        self.assertRaises(AttributeError, partial(z.send, None, None, None))

    def test_send_expects_connection_to_be_established(self):
        self.assertRaises(AttributeError, partial(Zmq().send, None, None, None))

    def test_send_passes_response_from_socket_recv_to_deferred_resolve(self):
        self.setUpConnect()
        self.socket.send(mox.IsA(str), mox.IsA(int))
        self.socket.send(mox.IsA(str))
        self.socket.recv().AndReturn('resp')
        self.deferred.resolve('resp')
        self.mox.ReplayAll()

        Zmq(context=self.ctx).connect().send('route', 'message',
                self.deferred)

        self.mox.VerifyAll()

    def test_serve_will_not_initialize_already_initialized_socket(self):
        self.setUpConnect()
        self.mox.ReplayAll()

        z = Zmq(context=self.ctx)
        z.connect()
        self.assertTrue(z.serve() is None)

        self.mox.VerifyAll()

    def test_serve_will_work_until_exception_raises(self):
        self.setUpBind()
        self.socket.recv().WithSideEffects(terminate_server)
        self.mox.ReplayAll()
        self.assertRaises(KeyboardInterrupt, Zmq(context=self.ctx).serve)
        self.mox.VerifyAll()

    def test_serve_expects_handler_for_given_route(self):
        self.setUpBind()
        self.socket.recv().AndReturn('route')
        self.socket.recv().AndReturn('msg')
        self.mox.ReplayAll()
        z = Zmq(context=self.ctx)
        self.assertRaises(KeyError, z.serve)
        self.mox.VerifyAll()

    def test_serve_deferred_instance_returned_from_handler(self):
        self.setUpBind()
        c = self.mox.CreateMockAnything()
        c(mox.IsA(str))
        self.socket.recv().AndReturn('route')
        self.socket.recv().AndReturn('msg')
        self.mox.ReplayAll()
        z = Zmq(context=self.ctx)
        z.attach_listener('route', c)
        self.assertRaises(AttributeError, z.serve)
        self.mox.VerifyAll()

    def test_serve_expects_zmq_messages_consisted_on_2_parts(self):
        self.setUpBind()
        c = self.mox.CreateMockAnything()
        c('msg').AndReturn(self.deferred)
        self.socket.recv().AndReturn('route')
        self.socket.recv().AndReturn('msg')
        self.deferred.done(mox.IsA(object)).WithSideEffects(terminate_server)
        self.mox.ReplayAll()
        z = Zmq(context=self.ctx)
        z.attach_listener('route', c)
        self.assertRaises(KeyboardInterrupt, z.serve)
        self.mox.VerifyAll()

def terminate_server(*args, **kwargs):
    raise KeyboardInterrupt()

if "__main__" == __name__:
    unittest.main()
