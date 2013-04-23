#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _path
_path.fix()
import sys

from pygrapes import Grape, serve

grape = Grape('local', adapter='pygrapes.adapter.Zmq')

@grape.task
def mul(a, b):
    print 'mul', a, b
    return a * b

@grape.sync
def add(a, b):
    print 'add', a, b
    return a + b

@grape.async
def sub(a, b, deferred):
    print 'sub', a, b
    deferred.resolve(a-b)

def main():
    def handler(ret):
        print ret

    def err(*args, **kwargs):
        print (args, kwargs)

    mul(2, 3).then(handler, err)
    add(1, 2).then(handler, err)
    sub(2, 3).then(handler, err)

if '__main__' == __name__:
    if len(sys.argv) > 1:
        serve()
    else:
        main()
