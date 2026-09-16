"""Asynchronous desktop telephone state machine (no real calls)."""

import time
import threading
import e32
import _device

(
    EStatusUnknown,
    EStatusIdle,
    EStatusDialling,
    EStatusRinging,
    EStatusAnswering,
    EStatusConnecting,
    EStatusConnected,
    EStatusReconnectPending,
    EStatusDisconnecting,
    EStatusHold,
    EStatusTransferring,
    EStatusTransferAlerting,
) = range(12)
_state = EStatusIdle
_number = ""
_callback = None
_owner = None
_pending = []
_armed = False
_incoming = False
_started = None


def _transition(state):
    global _state, _started
    _state = state
    if state == EStatusConnected:
        _started = time.time()
    cb = _callback
    if cb is not None:
        event = (state, _number if _incoming else "")
        e32._schedule(0, lambda: cb(event) if _callback is cb else None, owner=_owner)


def _queue(states):
    def step(index):
        _transition(states[index])
        if index + 1 < len(states):
            _pending.append(e32._schedule(0.01, lambda: step(index + 1)))

    _pending.append(e32._schedule(0, lambda: step(0)))


def _clear():
    for item in _pending:
        e32._cancel(item)
    _pending[:] = []


def dial(number):
    global _number, _incoming, _state, _started
    if _state != EStatusIdle:
        raise RuntimeError("call already active")
    _number = _device.number(number)
    _incoming, _started = False, None
    _state = EStatusDialling
    _queue([EStatusDialling, EStatusConnecting, EStatusConnected])


def hang_up():
    global _state
    if _state == EStatusIdle:
        raise RuntimeError("no active call")
    _clear()
    direction = ("in" if _started is not None else "missed") if _incoming else "out"
    _device.add_log(
        "call",
        direction,
        _number,
        duration=int(time.time() - _started) if _started else 0,
    )
    _state = EStatusDisconnecting
    _queue([EStatusDisconnecting, EStatusIdle])


def call_state(cb):
    global _callback, _owner
    if not callable(cb):
        raise TypeError("callback must be callable")
    _callback, _owner = cb, threading.current_thread().ident


def incoming_call():
    global _armed
    _armed = True


def answer():
    global _state
    if not _armed or _state != EStatusRinging:
        raise RuntimeError("no incoming call to answer")
    _state = EStatusAnswering
    _queue([EStatusAnswering, EStatusConnected])


def cancel():
    global _callback, _armed, _state
    _clear()
    _callback, _armed, _state = None, False, EStatusIdle


def _receive(number):
    global _number, _incoming, _started
    if _state != EStatusIdle:
        raise RuntimeError("call already active")
    _number, _incoming, _started = _device.number(number), True, None
    _transition(EStatusRinging)
