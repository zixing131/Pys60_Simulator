# -*- coding: utf-8 -*-
"""PyS60 DBM semantics using SQLite, including read-only and deferred writes.

Keys/values are byte strings; Unicode inputs are encoded with latin-1, as in
1.4.5. SQLite and old simulator JSON files are not Symbian DBMS binaries.
"""
import os
import sqlite3
import sys
from e32 import SymbianError
try:
    from collections.abc import MutableMapping
except ImportError:
    from collections import MutableMapping
try:
    text_type = unicode
except NameError:
    text_type = str
error = SymbianError
__all__ = ['error', 'open']


def _bytes(value):
    if isinstance(value, text_type):
        return value.encode('latin1')
    if isinstance(value, bytes):
        return value
    raise TypeError('Only string keys and values are accepted.')


class e32dbm(MutableMapping):
    def __init__(self, filename, flags):
        self.flags = flags
        self.fast = 'f' in flags
        self.pending_updates = {}
        try:
            self.db = sqlite3.connect(filename, isolation_level=None)
            if flags[0] in 'cn':
                self.db.execute('CREATE TABLE IF NOT EXISTS data (key BLOB PRIMARY KEY, value BLOB NOT NULL)')
            self.db.execute('SELECT key, value FROM data LIMIT 0')
        except sqlite3.Error as exc:
            if getattr(self, 'db', None) is not None:
                self.db.close()
            self.db = None
            raise SymbianError(-5, 'Unsupported or invalid database format: '+str(exc))

    def _check(self, write=False):
        if self.db is None:
            raise RuntimeError('Already closed')
        if write and self.flags[0] == 'r':
            raise IOError('Read-only database.')

    def __getitem__(self, key):
        self._check()
        key = _bytes(key)
        if key in self.pending_updates:
            result = self.pending_updates[key]
        else:
            row = self.db.execute('SELECT value FROM data WHERE key=?', (sqlite3.Binary(key),)).fetchone()
            result = bytes(row[0]) if row is not None else None
        if result is None:
            raise KeyError(key)
        return result

    def __setitem__(self, key, value):
        self._check(True)
        key, value = _bytes(key), _bytes(value)
        if self.fast:
            self.pending_updates[key] = value
        else:
            self.db.execute('INSERT OR REPLACE INTO data VALUES (?,?)', (sqlite3.Binary(key), sqlite3.Binary(value)))

    def __delitem__(self, key):
        self._check(True)
        key = _bytes(key)
        # Like the upstream SQL implementation, deleting a missing key is a no-op.
        if self.fast:
            self.pending_updates[key] = None
        else:
            self.db.execute('DELETE FROM data WHERE key=?', (sqlite3.Binary(key),))

    def keys(self):
        return [key for key, value in self.items()]

    def items(self):
        self._check()
        data = dict((bytes(k), bytes(v)) for k, v in self.db.execute('SELECT key,value FROM data'))
        data.update(self.pending_updates)
        return [(key, value) for key, value in data.items() if value is not None]

    def values(self):
        return [value for key, value in self.items()]

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return len(self.keys())

    def iterkeys(self):
        return iter(self.keys())

    def iteritems(self):
        return iter(self.items())

    def itervalues(self):
        return iter(self.values())

    def has_key(self, key):
        return key in self

    def clear(self):
        self._check(True)
        self.db.execute('DELETE FROM data')
        self.pending_updates.clear()

    def sync(self):
        self._check()
        if not self.pending_updates:
            return
        self.db.execute('BEGIN')
        try:
            for key, value in self.pending_updates.items():
                if value is None:
                    self.db.execute('DELETE FROM data WHERE key=?', (sqlite3.Binary(key),))
                else:
                    self.db.execute('INSERT OR REPLACE INTO data VALUES (?,?)', (sqlite3.Binary(key), sqlite3.Binary(value)))
            self.db.execute('COMMIT')
            self.pending_updates.clear()
        except Exception:
            self.db.execute('ROLLBACK')
            raise

    def reorganize(self):
        self._check(True)
        self.sync()
        self.db.execute('VACUUM')

    def close(self):
        self._check()
        self.sync()
        self.db.close()
        self.db = None

    def __del__(self):
        if getattr(self, 'db', None) is not None:
            self.close()


def open(name, flags='r', mode=0o666):
    if not flags or flags[0] not in 'cnrw' or any(flag != 'f' for flag in flags[1:]):
        raise TypeError('First flag must be one of c, n, r, w; optional suffix f.')
    filename = name if name.endswith('.e32dbm') else name+'.e32dbm'
    if flags[0] in 'rw' and not os.path.isfile(filename):
        raise SymbianError(-1, 'database not found')
    if flags[0] == 'n' and os.path.exists(filename):
        os.remove(filename)
    return e32dbm(filename, flags)
