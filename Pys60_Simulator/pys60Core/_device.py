"""Shared desktop device state. Nothing here sends traffic to a mobile network."""

import os
import json
import sqlite3
import time
import threading
import e32
from _compat import makedirs, fspath, string_types


def data_path(name):
    root = os.path.expanduser(os.environ.get("PYS60_DATA_DIR", "~/.pys60-simulator"))
    if not os.path.isdir(root):
        makedirs(root)
    return os.path.join(root, name)


def database_path(name, default):
    if name is None:
        return data_path(default)
    name = fspath(name)
    if not name:
        raise RuntimeError("invalid filename")
    if len(name) > 1 and name[1] == ":":
        return data_path(
            name[0].lower() + "/" + name[2:].replace("\\", "/").lstrip("/")
        )
    return os.path.abspath(name)


class Store:
    """Transactional JSON records, with stable integer IDs and safe encoding."""

    def __init__(self, path, mode="c"):
        if mode not in (None, "c", "n"):
            raise ValueError("invalid open mode")
        if mode is None and not os.path.exists(path):
            raise e32.SymbianError(-1, "database not found")
        makedirs(os.path.dirname(path))
        self.conn = sqlite3.connect(path)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS records (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT NOT NULL)"
        )
        if mode == "n":
            self.conn.execute("DELETE FROM records")
        self.conn.commit()

    def ids(self):
        return [r[0] for r in self.conn.execute("SELECT id FROM records ORDER BY id")]

    def get(self, key):
        if not isinstance(key, int):
            raise TypeError("integer id expected")
        row = self.conn.execute(
            "SELECT data FROM records WHERE id=?", (key,)
        ).fetchone()
        if row is None:
            raise KeyError(key)
        return json.loads(row[0])

    def put(self, key, value):
        value = json.dumps(value, ensure_ascii=False, allow_nan=True)
        with self.conn:
            if key:
                cur = self.conn.execute(
                    "UPDATE records SET data=? WHERE id=?", (value, key)
                )
                if not cur.rowcount:
                    raise KeyError(key)
            else:
                key = self.conn.execute(
                    "INSERT INTO records(data) VALUES (?)", (value,)
                ).lastrowid
        return key

    def delete(self, key):
        self.get(key)
        with self.conn:
            self.conn.execute("DELETE FROM records WHERE id=?", (key,))

    def compact(self):
        self.conn.execute("VACUUM")


def messages():
    return Store(data_path("messages.sqlite"))


def add_log(kind, direction, number="", name="", **extra):
    event = dict(
        number=number,
        name=name,
        description=kind,
        direction=direction,
        status="",
        subject="",
        contact=0,
        duration=0,
        flags=0,
        link=0,
        time=time.time(),
        data="",
        **{"duration type": 0}
    )
    event.update(extra)
    event["_type"] = kind
    store = Store(data_path("logs.sqlite"))
    key = store.put(0, event)
    store.conn.close()
    return key


def number(value):
    if isinstance(value, bytes):
        value = value.decode("ascii")
    if not isinstance(value, string_types):
        raise TypeError("telephone number must be a string")
    if len(value) > 30:
        raise ValueError("telephone number too long")
    return value


gsm = None
position_fix = None
camera_source = None
sensor_definitions = {"Accelerometer": {"id": 1, "category": 1}}
