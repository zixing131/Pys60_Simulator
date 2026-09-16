# -*- coding: utf-8 -*-
"""PyS60 database API over SQLite (not Symbian DBMS file-format compatible).

Simple table SELECTs preserve declared Symbian column types. SQL expressions
and joins use SQLite result types. Date literals are the ISO strings produced
by format_time/format_rawtime, surrounded by # as on PyS60.
"""
import datetime
import os
import re
import sqlite3
import struct
import time
from e32 import SymbianError
try:
    from builtins import open  # compatibility with old simulator callers
except ImportError:
    from __builtin__ import open

_EPOCH = 62168256000000000
_TYPES = {'BIT': 0, 'TINYINT': 1, 'UNSIGNED TINYINT': 2, 'SMALLINT': 3,
          'UNSIGNED SMALLINT': 4, 'INTEGER': 5, 'INT': 5, 'UNSIGNED INTEGER': 6,
          'COUNTER': 6, 'BIGINT': 7, 'REAL': 8, 'FLOAT': 9, 'DOUBLE': 9,
          'DOUBLE PRECISION': 9, 'DATE': 10, 'TIME': 10, 'TIMESTAMP': 10,
          'CHAR': 12, 'VARCHAR': 12, 'TEXT': 12, 'BINARY': 13, 'VARBINARY': 13,
          'BLOB': 13, 'LONG VARCHAR': 15, 'LONG VARBINARY': 16}


def format_time(timevalue):
    # The upstream conversion truncates Unix time to whole seconds.
    return datetime.datetime.fromtimestamp(int(timevalue)).strftime('%Y-%m-%d %H:%M:%S.%f')


def format_rawtime(timevalue):
    value = datetime.datetime(1970, 1, 1)+datetime.timedelta(microseconds=int(timevalue)-_EPOCH)
    return value.strftime('%Y-%m-%d %H:%M:%S.%f')


def _date(value):
    for pattern in ('%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d-%b/%Y'):
        try:
            return datetime.datetime.strptime(value, pattern)
        except ValueError:
            continue
    raise SymbianError(-6, 'invalid SQL date literal')


def _sql(query):
    # Only rewrite outside SQL quoted strings, so text containing # survives.
    tokens = re.split("('(?:[^']|'')*')", query)
    for i in range(0, len(tokens), 2):
        tokens[i] = re.sub(r'#([^#]+)#', lambda m: "'"+_date(m.group(1)).strftime('%Y-%m-%d %H:%M:%S.%f')+"'", tokens[i])
    return ''.join(tokens)


class Dbms(object):
    def __init__(self):
        self._connection = None

    def _db(self):
        if self._connection is None:
            raise RuntimeError('Database is not open')
        return self._connection

    def create(self, dbname):
        # Native Replace() creates or replaces the named database, then closes it.
        self.close()
        if os.path.exists(dbname):
            os.remove(dbname)
        connection = sqlite3.connect(dbname)
        connection.execute('PRAGMA user_version=1')
        connection.close()

    def open(self, dbname):
        self.close()
        if not os.path.isfile(dbname):
            raise SymbianError(-1, 'database not found')
        try:
            self._connection = sqlite3.connect(dbname, isolation_level=None)
            self._connection.execute('PRAGMA schema_version')
        except sqlite3.Error as exc:
            self.close()
            raise SymbianError(-5, 'Only simulator SQLite databases are supported: '+str(exc))

    def close(self):
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def execute(self, query):
        try:
            cursor = self._db().execute(_sql(query))
            return max(0, cursor.rowcount)
        except sqlite3.Error as exc:
            raise SymbianError(-6, str(exc))

    def begin(self):
        self.execute('BEGIN')

    def commit(self):
        self.execute('COMMIT')

    def rollback(self):
        self.execute('ROLLBACK')

    def compact(self):
        self.execute('VACUUM')


class Db_view(object):
    def __init__(self):
        self._rows = None
        self._ready = False

    def prepare(self, db, query):
        if not isinstance(db, Dbms):
            raise TypeError('Dbms object expected')
        self._rows = None
        self._ready = False
        try:
            cursor = db._db().execute(_sql(query))
            if cursor.description is None:
                raise SymbianError(-6, 'SELECT statement expected')
            names = [column[0].lower() for column in cursor.description]
            self._rows = cursor.fetchall()
            declared = {}
            table = re.search(r'\bFROM\s+([\w]+)', query, re.I)
            if table:
                for col in db._db().execute('PRAGMA table_info("%s")' % table.group(1)):
                    typename = re.sub(r'\(.*\)', '', col[2]).strip().upper()
                    declared[col[1].lower()] = _TYPES.get(typename, 12)
            self._types = []
            for i, name in enumerate(names):
                kind = declared.get(name)
                if kind is None:
                    value = next((row[i] for row in self._rows if row[i] is not None), None)
                    kind = 7 if isinstance(value, int) else 9 if isinstance(value, float) else 13 if isinstance(value, bytes) else 12
                self._types.append(kind)
            self._index = 0
        except sqlite3.Error as exc:
            raise SymbianError(-6, str(exc))

    def _prepared(self):
        if self._rows is None:
            raise RuntimeError('View is not prepared')

    def _column(self, column, ready=True):
        self._prepared()
        if not isinstance(column, int):
            raise TypeError('integer expected')
        if not 1 <= column <= len(self._types):
            raise RuntimeError('Invalid column number')
        if ready and (not self._ready or not 0 <= self._index < len(self._rows)):
            raise RuntimeError('No current row; call get_line() first')
        return column-1

    def first_line(self):
        self._prepared()
        self._index, self._ready = 0, False

    def next_line(self):
        self._prepared()
        if self._index >= len(self._rows):
            raise RuntimeError('End of view, there is no next line.')
        self._index += 1
        self._ready = False

    def get_line(self):
        self._prepared()
        if not 0 <= self._index < len(self._rows):
            raise RuntimeError('Not at a row')
        self._ready = True

    def count_line(self):
        self._prepared()
        return len(self._rows)

    def col_count(self):
        self._prepared()
        return len(self._types)

    def col_type(self, column):
        return self._types[self._column(column)]

    def is_col_null(self, column):
        return self._rows[self._index][self._column(column)] is None

    def col(self, column):
        index = self._column(column)
        value, kind = self._rows[self._index][index], self._types[index]
        if kind == 16:
            raise TypeError('LONG VARBINARY is not supported')
        if value is None:
            return u'' if kind in (12, 15) else b'' if kind == 13 else 0.0 if kind in (8, 9, 10) else 0
        if kind == 10:
            date = _date(value)
            return time.mktime(date.timetuple())+date.microsecond/1000000.0
        if kind in (8, 9):
            return float(value)
        if kind < 8:
            return int(value)
        return value

    def col_length(self, column):
        if self.is_col_null(column):
            return 0
        value = self.col(column)
        return len(value) if self.col_type(column) in (12, 13, 15) else 1

    def col_rawtime(self, column):
        index = self._column(column)
        if self._types[index] != 10:
            raise TypeError('Column must be of date/time type.')
        value = self._rows[self._index][index]
        if value is None:
            return 0
        delta = _date(value)-datetime.datetime(1970, 1, 1)
        return _EPOCH+(delta.days*86400+delta.seconds)*1000000+delta.microseconds

    def col_raw(self, column):
        kind = self.col_type(column)
        if kind in (15, 16):
            raise TypeError("This function doesn't support LONG columns.")
        if self.is_col_null(column):
            return b''
        value = self.col(column)
        if kind == 12:
            return value.encode('utf-16-le')
        if kind == 13:
            return value
        if kind == 10:
            return struct.pack('<q', self.col_rawtime(column))
        formats = {0: 'B', 1: 'b', 2: 'B', 3: 'h', 4: 'H', 5: 'i', 6: 'I', 7: 'q', 8: 'f', 9: 'd'}
        return struct.pack('<'+formats[kind], value)
