#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "mib"
__date__ = "$2011-01-22 12:02:41$"

from pygrapes.util import not_implemented
from pygrapes.adapter.abstract import Abstract
from pygrapes.adapter.local import Local

try:
    from pygrapes.adapter.zeromq import Zmq
except ImportError:
    Zmq = not_implemented('A working pyzmq lib is required!')

try:
    from pygrapes.adapter.amqp import Amqp
except ImportError:
    Amqp = not_implemented('A working amqplib lib is required!')


__all__ = ['Abstract', 'Amqp', 'Local', 'Zmq']
