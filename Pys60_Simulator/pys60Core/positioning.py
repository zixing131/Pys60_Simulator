"""Thread-local GPS requests with PyS60 event shapes and microsecond intervals."""

import copy
import threading
import time
import e32
import _device

POSITION_INTERVAL = 1000000
_tls = threading.local()
_MODULE = 0x50595360


def modules():
    return [
        {
            "id": _MODULE,
            "available": _device.position_fix is not None,
            "name": "Desktop GPS feed",
        }
    ]


def default_module():
    return _MODULE


def module_info(module_id):
    if module_id != _MODULE:
        raise e32.SymbianError(-1, "positioning module not found")
    return dict(
        id=_MODULE,
        available=_device.position_fix is not None,
        name="Desktop GPS feed",
        technology=0,
        location=0,
        capabilities=7,
        version="1.0",
        position_quality=dict(
            horizontal_accuracy=0.0,
            vertical_accuracy=0.0,
            power_consumption=0,
            cost=0,
            time_to_next_fix=0,
            time_to_first_fix=0,
        ),
        status=dict(
            device_status=7 if _device.position_fix else 3,
            data_quality=3 if _device.position_fix else 0,
        ),
    )


def select_module(module_id):
    module_info(module_id)
    stop_position()
    _tls.module = module_id


def set_requestors(requestors):
    if not isinstance(requestors, list):
        raise TypeError("requestors must be a list")
    if not requestors:
        raise SyntaxError("no requestors given in the list")
    result = copy.deepcopy(requestors)
    for item in result:
        if item["type"] not in ("service", "contact"):
            raise KeyError(item["type"])
        if item["format"] not in ("application", "telephone", "url", "email"):
            raise KeyError(item["format"])
        item["data"] = str(item["data"])
    _tls.requestors = result


def stop_position():
    e32._cancel(getattr(_tls, "pending", None))
    _tls.pending, _tls.ongoing = None, False
    _tls.generation = getattr(_tls, "generation", 0) + 1


def _sample(course, satellites):
    if _device.position_fix is None:
        raise e32.SymbianError(-18, "GPS feed is not configured")
    result = copy.deepcopy(_device.position_fix)
    _tls.last = dict(result["position"], time=result.get("time", time.time()))
    return dict(
        position=result["position"],
        course=result.get("course") if course else None,
        satellites=result.get("satellites") if satellites else None,
    )


def position(
    course=0, satellites=0, callback=None, interval=POSITION_INTERVAL, partial=0
):
    if getattr(_tls, "ongoing", False):
        raise RuntimeError("Position request ongoing")
    if callback is not None and not callable(callback):
        raise TypeError("callback must be callable")
    if not isinstance(interval, int):
        raise TypeError("integer interval expected")
    if interval < 0:
        raise ValueError("interval must be nonnegative")
    if not getattr(_tls, "requestors", None):
        raise e32.SymbianError(-46, "requestors not set")
    if _device.position_fix is None:
        raise e32.SymbianError(-18, "GPS feed is not configured")
    _tls.ongoing = True
    generation = getattr(_tls, "generation", 0)
    result = []

    def tick():
        if not _tls.ongoing or generation != getattr(_tls, "generation", 0):
            return
        event = _sample(course, satellites)
        if callback is None:
            result.append(event)
        else:
            _tls.pending = e32._schedule(max(interval / 1000000.0, 0.001), tick)
            callback(event)

    _tls.pending = e32._schedule(0, tick)
    if callback is None:
        try:
            e32._wait_until(lambda: bool(result))
            return result[0]
        finally:
            stop_position()


def last_position():
    if getattr(_tls, "ongoing", False):
        raise RuntimeError("Position request ongoing")
    if not hasattr(_tls, "last"):
        raise e32.SymbianError(-1, "no previous position")
    return copy.deepcopy(_tls.last)
