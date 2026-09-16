"""Persistent simulated Symbian message folders."""
from _compat import text_type as str

import time
import weakref
import threading
import e32
import _device

EInbox, EOutbox, EDraft, ESent = 0x1002, 0x1003, 0x1004, 0x1005
_listeners = weakref.WeakSet()


class Inbox:
    def __init__(self, folder_type=EInbox):
        if folder_type not in (EInbox, EOutbox, EDraft, ESent):
            raise e32.SymbianError(-1, "folder not found")
        self._folder = folder_type
        self._callback = None
        self._owner = threading.current_thread().ident
        _listeners.add(self)

    def _get(self, message_id):
        store = _device.messages()
        try:
            value = store.get(message_id)
            if value.get("kind") != "sms":
                raise KeyError(message_id)
            return value
        except KeyError:
            raise e32.SymbianError(-1, "message not found")
        finally:
            store.conn.close()

    def sms_messages(self):
        store = _device.messages()
        try:
            return [
                k
                for k in reversed(store.ids())
                if store.get(k)["folder"] == self._folder
                and store.get(k)["kind"] == "sms"
            ]
        finally:
            store.conn.close()

    def content(self, sms_id):
        return self._get(sms_id)["content"][:511]

    def address(self, sms_id):
        return self._get(sms_id)["address"][:511]

    def time(self, sms_id):
        return self._get(sms_id)["time"]

    def unread(self, sms_id):
        return int(self._get(sms_id)["unread"])

    def set_unread(self, sms_id, unread):
        if unread not in (0, 1):
            raise ValueError("unread must be 0 or 1")
        value = self._get(sms_id)
        value["unread"] = bool(unread)
        store = _device.messages()
        try:
            store.put(sms_id, value)
        finally:
            store.conn.close()

    def delete(self, sms_id):
        self._get(sms_id)
        store = _device.messages()
        try:
            store.delete(sms_id)
        finally:
            store.conn.close()

    def bind(self, callback):
        if callback is not None and not callable(callback):
            raise TypeError("callback must be callable or None")
        self._callback = callback


def _receive(number, content, timestamp=None):
    number = _device.number(number)
    store = _device.messages()
    key = store.put(
        0,
        dict(
            kind="sms",
            folder=EInbox,
            address=number,
            content=str(content),
            time=time.time() if timestamp is None else float(timestamp),
            unread=True,
        ),
    )
    store.conn.close()
    _device.add_log("sms", "in", number, subject=str(content))
    for listener in list(_listeners):
        callback = listener._callback
        if callback is not None:
            ref = weakref.ref(listener)

            def notify(ref=ref, callback=callback):
                obj = ref()
                if obj is not None and obj._callback is callback:
                    callback(key)

            e32._schedule(0, notify, owner=listener._owner)
    return key
