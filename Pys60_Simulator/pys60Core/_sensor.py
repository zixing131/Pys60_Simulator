"""Device event transport used by the unmodified Nokia sensor filters."""

import copy
import threading
import weakref
import _device
import e32

_connections = weakref.WeakSet()


def sensors():
    return copy.deepcopy(_device.sensor_definitions)


class sensor:
    def __init__(self, sensor_id, category_id):
        if {"id": sensor_id, "category": category_id} not in list(sensors().values()):
            raise e32.SymbianError(-1, "sensor not found")
        self.id, self.callback, self.owner = sensor_id, None, threading.current_thread().ident

    def connect(self, callback):
        if not callable(callback):
            raise TypeError("callback must be callable")
        if self.callback is not None:
            return 0
        self.callback = callback
        _connections.add(self)
        return 1

    def disconnect(self):
        if self.callback is None:
            return 0
        self.callback = None
        _connections.discard(self)
        return 1


def _emit(sensor_id, data_1, data_2, data_3):
    data = dict(sensor_id=sensor_id, data_1=data_1, data_2=data_2, data_3=data_3)
    if any(not isinstance(v, int) for v in data.values()):
        raise TypeError("sensor data must be integers")
    for obj in list(_connections):
        if obj.id != sensor_id:
            continue
        callback, ref = obj.callback, weakref.ref(obj)

        def notify(ref=ref, callback=callback):
            obj = ref()
            if obj is not None and obj.callback is callback:
                callback(dict(data))

        e32._schedule(0, notify, owner=obj.owner)
