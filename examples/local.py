#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _path
_path.fix()

from pygrapes.tasks import setup_task_group, serve
from pygrapes.adapter import Local
from pygrapes.serializer.json import Json


task = setup_task_group('local', adapter=Local(), serializer=Json())

@task
def add(a, b, deferred):
    deferred.resolve(a + b)

serve('local')

def handler(ret):
    print ret

def err(*args, **kwargs):
    print (args, kwargs)

add(1, 2).then(handler, err)
