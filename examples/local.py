#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _path
_path.fix()

from pygrapes import Grape, serve

grape = Grape('local', adapter='pygrapes.adapter.Local')

@grape.task
def mul(a, b):
    return a * b

@grape.sync
def add(a, b):
    return a + b

@grape.async
def sub(a, b, deferred):
    deferred.resolve(a-b)

# called only when current instance should "serve" requests
serve()

def handler(ret):
    print ret

def err(*args, **kwargs):
    print (args, kwargs)

mul(2, 3).then(handler, err)
add(1, 2).then(handler, err)
sub(2, 3).then(handler, err)
