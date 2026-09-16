# -*- coding: utf-8 -*-
"""Install the S60 access-point API on the host socket module.

A single desktop access point uses the host's existing network configuration;
start/stop manage its simulator handle, not the host network adapter.
"""
import numbers
import socket
import e32

_default_access_point = None


class AccessPoint(object):
    def __init__(self, apid):
        self._id = apid
        self._started = False

    def start(self):
        if self._id != 1:
            raise e32.SymbianError(-1, 'access point not found')
        self._started = True

    def stop(self):
        self._started = False

    def ip(self):
        if not self._id:
            raise socket.error('Default access point is not set')
        if self._id != 1:
            raise e32.SymbianError(-1, 'access point not found')
        return socket.gethostbyname(socket.gethostname())


def access_point(apid):
    if not isinstance(apid, numbers.Integral):
        raise TypeError('integer expected')
    if apid <= 0:
        raise ValueError('illegal access point id')
    return AccessPoint(apid)


def access_points():
    return [{'iapid': 1, 'name': u'Desktop network'}]


def select_access_point():
    import appuifw
    points = access_points()
    selected = appuifw.selection_list([point['name'] for point in points])
    return None if selected is None else points[selected]['iapid']


def set_default_access_point(point):
    global _default_access_point
    if point is not None and not isinstance(point, AccessPoint):
        raise ValueError('Parameter must be access point object or None')
    if point is None and _default_access_point is not None:
        _default_access_point._id = 0
        _default_access_point._started = False
    _default_access_point = point


functions = ['access_point', 'access_points', 'select_access_point', 'set_default_access_point']
for name in functions:
    setattr(socket, name, globals()[name])

# Only AF_BT calls use the local virtual transport; Internet sockets retain the
# host implementation. Import appuifw (or this module) before using S60 helpers.
import _bluetooth
_bluetooth.install()
