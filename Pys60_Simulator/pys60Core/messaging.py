"""SMS/MMS lifecycle backed by the simulator's local message store."""

import os
import time
import e32
import _device
import inbox

ECreated, EMovedToOutBox, EScheduledForSend, ESent, EDeleted = range(5)
EScheduleFailed, ESendFailed, ENoServiceCentre, EFatalServerError = range(5, 9)
_sending = False


def sms_send(number, msg, encoding="7bit", callback=None, name=""):
    global _sending
    if _sending:
        raise RuntimeError("Already sending")
    number = _device.number(number)
    if encoding not in ("7bit", "8bit", "UCS2"):
        raise KeyError(encoding)
    if callback is not None and not callable(callback):
        raise TypeError("callback must be callable")
    msg, name = str(msg), str(name)
    if len(msg) > 39015 or len(name) > 60:
        raise ValueError("message or name too long")
    record = dict(
        kind="sms",
        folder=inbox.EDraft,
        address=number,
        content=msg,
        name=name,
        encoding=encoding,
        unread=False,
        time=time.time(),
    )
    store = _device.messages()
    key = store.put(0, record)
    store.conn.close()
    _sending = True
    lock = e32.Ao_lock()

    def event(state):
        global _sending
        if state == EMovedToOutBox:
            record["folder"] = inbox.EOutbox
        if state == ESent:
            record["folder"] = inbox.ESent
            _device.add_log("sms", "out", number, name, subject=msg)
        if state in (EMovedToOutBox, ESent):
            store = _device.messages()
            store.put(key, record)
            store.conn.close()
        if state == EDeleted:
            _sending = False
        else:
            e32._schedule(0.001, lambda: event(state + 1))
        try:
            if callback is not None:
                callback(state)
        finally:
            if callback is not None or state == EDeleted:
                lock.signal()

    e32._schedule(0, lambda: event(ECreated))
    lock.wait()


def mms_send(number, msg, attachment=None):
    number = _device.number(number)
    if attachment and not os.path.isfile(attachment):
        raise e32.SymbianError(-1, "attachment not found")
    store = _device.messages()
    store.put(
        0,
        dict(
            kind="mms",
            folder=inbox.ESent,
            address=number,
            content=str(msg),
            attachment=attachment,
            time=time.time(),
            unread=False,
        ),
    )
    store.conn.close()
