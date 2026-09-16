# -*- coding: utf-8 -*-
"""PyS60 key capture restricted to the simulator window, not host-wide keys."""
import numbers
import weakref
import key_codes
from key_codes import *

all_keys = [getattr(key_codes, name) for name in dir(key_codes) if not name.startswith('_')]
_capturers = weakref.WeakSet()


class KeyCapturer(object):
    def __init__(self, callback):
        if not callable(callback):
            raise TypeError('callable expected')
        self._callback = callback
        self._keys = []
        self._forwarding = 0
        self._last = 0
        self._listening = False

    def _set_keys(self, values):
        values = list(values)
        if any(not isinstance(value, numbers.Integral) for value in values):
            raise TypeError('integer key codes expected')
        self._keys = list(dict.fromkeys(values))

    keys = property(lambda self: self._keys[:], _set_keys)
    forwarding = property(lambda self: self._forwarding,
                          lambda self, value: setattr(self, '_forwarding', int(value)))

    def start(self):
        self._listening = True
        _capturers.add(self)

    def stop(self):
        self._listening = False
        _capturers.discard(self)

    def last_key(self):
        return self._last


def _dispatch(code):
    consumed = False
    for capturer in list(_capturers):
        if capturer._listening and code in capturer._keys:
            capturer._last = code
            capturer._callback(code)
            consumed = consumed or not capturer.forwarding
    return consumed
