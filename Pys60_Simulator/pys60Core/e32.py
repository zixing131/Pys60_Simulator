# -*- coding: utf-8 -*-
"""Desktop implementation of the PyS60 1.4.5 active-object contract.

Callbacks run on their creator thread when it enters the active scheduler,
never on a threading.Timer thread (which cannot safely operate Tk).
"""
import heapq
import itertools
import math
import os
import shlex
import shutil
import subprocess
import sys
import threading
import time
import traceback
import weakref

try:
    import builtins
except ImportError:
    import __builtin__ as builtins

class SymbianError(OSError):
    pass

if not hasattr(builtins, 'SymbianError'):
    builtins.SymbianError = SymbianError

s60_version_info = (3, 0)
pys60_version_info = (1, 4, 5, 'final', 0)
pys60_version = '1.4.5 final (desktop simulator)'
_clock = getattr(time, 'monotonic', time.time)
_ui_thread = threading.current_thread().ident
_queues = {}
_mutex = threading.RLock()
_sequence = itertools.count()
_missing = object()
_last_activity = _clock()


def _schedule(delay, callback, owner=None):
    if owner is None:
        owner = threading.current_thread().ident
    item = [_clock() + delay, next(_sequence), callback]
    with _mutex:
        heapq.heappush(_queues.setdefault(owner, []), item)
    return item


def _cancel(item):
    if item is not None:
        item[2] = None


def _pump():
    owner = threading.current_thread().ident
    # Keep other ready callbacks in the queue: a callback may enter a nested
    # Ao_lock.wait() that depends on one of them. Limit this pass by time so
    # self-rescheduling zero-delay callbacks cannot starve the UI.
    now = _clock()
    while True:
        with _mutex:
            queue = _queues.setdefault(owner, [])
            if not queue or queue[0][0] > now:
                break
            item = heapq.heappop(queue)
        callback, item[2] = item[2], None
        if callback is not None:
            try:
                callback()
            except Exception:
                traceback.print_exc()


def ao_yield():
    _pump()
    module = sys.modules.get('appuifw')
    if module is not None and is_ui_thread():
        module.app._pump_ui()
    time.sleep(0)


def _wait_until(predicate):
    while not predicate():
        ao_yield()
        if not predicate():
            time.sleep(0.001)


def _delay(value):
    if not isinstance(value, (int, float)):
        raise TypeError('a number is required')
    value = float(value)
    if value < 0:
        raise RuntimeError('negative number not allowed')
    if math.isnan(value) or math.isinf(value):
        raise ValueError('interval must be finite')
    return value


class Ao_lock(object):
    def __init__(self):
        self._owner = threading.current_thread().ident
        self._event = threading.Event()
        self._waiting = False

    def wait(self):
        if threading.current_thread().ident != self._owner:
            raise AssertionError('Ao_lock.wait must be called from lock creator thread')
        if self._waiting:
            raise AssertionError('wait() already in progress')
        self._waiting = True
        try:
            _wait_until(self._event.is_set)
            self._event.clear()
        finally:
            self._waiting = False

    def signal(self):
        self._event.set()


class Ao_timer(object):
    def __init__(self):
        self._pending = None
        self._owner = threading.current_thread().ident

    def cancel(self):
        _cancel(self._pending)
        self._pending = None

    def after(self, interval, callback=_missing):
        delay = _delay(interval)
        if callback is not _missing and not callable(callback):
            raise TypeError('callable expected for 2nd argument')
        if self._pending is not None:
            raise RuntimeError('Timer pending - cancel first')
        reference = weakref.ref(self)
        def done():
            timer = reference()
            if timer is None:
                return
            timer._pending = None
            if callback is not _missing:
                callback()
        self._pending = _schedule(delay, done, self._owner)
        if callback is _missing:
            _wait_until(lambda: self._pending is None)

    def __del__(self):
        self.cancel()


def ao_sleep(interval, callback=_missing):
    delay = _delay(interval)
    if callback is _missing:
        deadline = _clock() + delay
        ao_yield()
        _wait_until(lambda: _clock() >= deadline)
    else:
        if not callable(callback):
            raise TypeError('callable expected for 2nd argument')
        _schedule(delay, callback)


def ao_callgate(wrapped_callable):
    if not callable(wrapped_callable):
        raise TypeError('callable expected')
    owner = threading.current_thread().ident
    def callgate(*args, **kwargs):
        _schedule(0, lambda: wrapped_callable(*args, **kwargs), owner)
    return callgate


def drive_list():
    if os.name == 'nt':
        return [chr(c) + ':' for c in range(65, 91) if os.path.isdir(chr(c) + ':\\')]
    # A single host filesystem, presented as the emulator's C drive.
    return [u'C:']


def file_copy(target_name, source_name):
    shutil.copyfile(source_name, target_name)


def in_emulator():
    return True


def is_ui_thread():
    return threading.current_thread().ident == _ui_thread


def reset_inactivity():
    global _last_activity
    _last_activity = _clock()


def inactivity():
    return int(_clock() - _last_activity)


def set_home_time(value):
    float(value)
    raise SymbianError(-5, 'Setting the host system clock is not supported')


def start_exe(filename, command, wait=0):
    process = subprocess.Popen([filename] + shlex.split(command))
    if wait:
        return 0 if process.wait() == 0 else 2


def start_server(filename):
    subprocess.Popen([sys.executable, filename])


def strerror(code):
    errors = {0: 'KErrNone', -1: 'KErrNotFound', -2: 'KErrGeneral',
              -3: 'KErrCancel', -4: 'KErrNoMemory', -5: 'KErrNotSupported',
              -6: 'KErrArgument', -11: 'KErrAlreadyExists', -14: 'KErrInUse',
              -18: 'KErrNotReady', -21: 'KErrAccessDenied', -22: 'KErrLocked',
              -25: 'KErrEof', -26: 'KErrDiskFull', -33: 'KErrTimedOut',
              -46: 'KErrPermissionDenied'}
    return errors.get(code, 'Symbian error %d' % code)
