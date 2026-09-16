"""Small host-version adapters; PyS60 applications retain Python 2 semantics."""
import os
import sys

PY2 = sys.version_info[0] == 2
try:
    text_type = unicode
    string_types = (basestring,)
except NameError:
    text_type = str
    string_types = (str,)


def makedirs(path):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise


def fspath(value):
    return value.__fspath__() if hasattr(value, '__fspath__') else value


def casefold(value):
    return value.casefold() if hasattr(value, 'casefold') else value.lower()


def timestamp(value):
    import time
    import calendar
    offset = value.utcoffset()
    if offset is not None:
        return calendar.timegm(value.utctimetuple()) + value.microsecond / 1000000.0
    return time.mktime(value.timetuple()) + value.microsecond / 1000000.0
