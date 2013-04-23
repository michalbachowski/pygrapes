#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

try:
    from unittest import mock
except ImportError:
    import mock


def fix():
    p = os.path.join(os.path.dirname(__file__), '../src/')
    if p not in sys.path:
        sys.path.insert(0, p)


if "__main__" == __name__:
    fix()
