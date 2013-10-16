#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# test hepers
#
from testutils import mock

##
# python standard library
#
from functools import partial
import unittest

##
# ZeroMQ modules
try:
    import zmq
except ImportError:
    zmq = None

##
# pygrapes modules
#
from mock_helper import results
from pygrapes.adapter import Zmq


@unittest.skipIf(zmq is None, 'Missing zmq Python library')
class ZmqAdapterTestCase(unittest.TestCase):

    def setUp(self):
        self.ctx = mock.Mock()
        self.socket = mock.Mock()
        self.deferred = mock.Mock()

    def setUpConnect(self):
        self.ctx.socket = mock.MagicMock(return_value=self.socket)

    def setUpBind(self):
        self.ctx.socket = mock.MagicMock(return_value=self.socket)

    def test_init_expects_no_args(self):
        self.assertFalse(Zmq() is None)

    def test_init_allows_to_pass_config_arg(self):
        self.assertFalse(Zmq(config={}) is None)

    def test_init_allows_to_pass_context_arg(self):
        self.assertFalse(Zmq(context='foo') is None)

    def test_connects_expects_valid_context_instance(self):
        self.assertRaises(TypeError, Zmq().connect())

    def test_connects_expects_valid_context_instance_1(self):
        self.setUpConnect()
        Zmq(context=self.ctx).connect()
        self.ctx.socket.assert_called_once_with(IsA(int))
        self.socket.connect.assert_called_once_with(IsA(str))

    def test_connect_return_instance_of_self(self):
        self.assertTrue(isinstance(Zmq(context=self.ctx).connect(), Zmq))

    def test_connect_will_not_instantinate_socket_twice(self):
        self.setUpConnect()

        z = Zmq(context=self.ctx)
        self.assertTrue(isinstance(z.connect(), Zmq))
        self.assertTrue(isinstance(z.connect(), Zmq))
        self.ctx.socket.assert_called_once_with(IsA(int))
        self.socket.connect.assert_called_once_with(IsA(str))

    def test_connects_expects_valid_config_instance(self):
        self.assertRaises(AttributeError,
                Zmq(context=self.ctx, config='a').connect)

    def test_connects_expects_valid_config_instance_1(self):
        self.setUpConnect()
        cfg = mock.Mock()
        cfg.iteritems = mock.MagicMock(return_value = [])

        Zmq(context=self.ctx, config=cfg).connect()
        cfg.iteritems.assert_called_once_with()

    def test_connects_triggers_socket_configuration(self):
        self.setUpConnect()
        cfg = mock.Mock()
        cfg.iteritems = mock.MagicMock(return_value = {'a': 1}.iteritems())

        Zmq(context=self.ctx, config=cfg).connect()

        self.socket.setsockopt.assert_called_once_with('a', 1)


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
        self.socket.recv = mock.MagicMock(return_value = 'resp')

        Zmq(context=self.ctx).connect().send('route', 'message',
                self.deferred)

        expected = [mock.call(IsA(str), IsA(int)), mock.call(IsA(str))]
        self.assertEqual(self.socket.send.call_args_list, expected)
        self.socket.recv.assert_called_once_with()
        self.deferred.resolve.assert_called_once_with('resp')


    def test_serve_will_not_initialize_already_initialized_socket(self):
        self.setUpConnect()

        z = Zmq(context=self.ctx)
        z.connect()
        self.assertTrue(z.serve() is None)
        self.socket.connect.assert_called_once_with(IsA(str))
        self.assertEqual(self.socket.bind.call_count, 0)

    def test_serve_will_work_until_exception_raises(self):
        self.setUpBind()
        self.socket.recv = mock.MagicMock(side_effect=KeyboardInterrupt)
        self.assertRaises(KeyboardInterrupt, Zmq(context=self.ctx).serve)

        self.socket.bind.assert_called_once_with(IsA(str))
        self.socket.recv_assert_called_once_with()

    def test_serve_expects_handler_for_given_route(self):
        self.setUpBind()

        self.socket.recv = mock.MagicMock(side_effect=results('route', 'msg'))
        z = Zmq(context=self.ctx)
        self.assertRaises(KeyError, z.serve)

        expected = [mock.call(), mock.call()]
        self.assertEqual(self.socket.recv.call_args_list, expected)

    def test_serve_expects_deferred_instance_returned_from_handler(self):
        self.setUpBind()
        c = mock.MagicMock(return_value=self.deferred)

        self.socket.recv = mock.MagicMock(side_effect=results('route', 'msg',
                KeyboardInterrupt()))

        z = Zmq(context=self.ctx)
        z.attach_listener('route', c)
        self.assertRaises(KeyboardInterrupt, z.serve)

        c.assert_called_once_with(IsA(str))
        self.deferred.done.assert_called_once_with(IsCallable())

    def test_serve_expects_zmq_messages_consisted_on_2_parts(self):
        self.setUpBind()
        c = mock.MagicMock(return_value=self.deferred)

        self.socket.recv = mock.MagicMock(side_effect=results('route', 'msg'))
        self.deferred.done = mock.MagicMock(side_effect=KeyboardInterrupt)
        z = Zmq(context=self.ctx)
        z.attach_listener('route', c)
        self.assertRaises(KeyboardInterrupt, z.serve)

        c.assert_called_once_with(IsA(str))


if "__main__" == __name__:
    unittest.main()
