# -*- coding: utf-8 -*-
"""Opt-in portable files/text for bundled examples, on Python 2.7 and 3."""
import os
import shutil
import ast
from _compat import text_type, makedirs


def to_text(value, encoding='utf-8', errors='strict'):
    if isinstance(value, text_type):
        return value
    if isinstance(value, bytes):
        return value.decode(encoding, errors)
    return text_type(value)


def resource_path(*parts):
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(root, 'python', *parts)


def data_path(name, seed=None):
    root = os.path.expanduser(os.environ.get('PYS60_DATA_DIR', '~/.pys60-simulator'))
    destination = os.path.join(root, 'examples', name)
    makedirs(destination)
    if seed is not None:
        for directory, dirs, files in os.walk(seed):
            target_directory = os.path.join(destination, os.path.relpath(directory, seed))
            makedirs(target_directory)
            for filename in files:
                source = os.path.join(directory, filename)
                target = os.path.join(target_directory, filename)
                if not os.path.exists(target):
                    shutil.copy2(source, target)
                    if target.endswith('.e32dbm'):
                        _import_example_database(target)
    return destination


def _import_example_database(path):
    """Import old repr/JSON fixtures into the copied save directory only."""
    with open(path, 'rb') as stream:
        raw = stream.read()
    if raw.startswith(b'SQLite format 3'):
        return
    entries = dict(ast.literal_eval(raw.decode('utf-8')))
    import e32dbm
    temporary = path + '.import.e32dbm'
    db = e32dbm.open(temporary, 'n')
    try:
        for key, value in entries.items():
            db[to_text(key).encode('utf-8')] = to_text(value).encode('utf-8')
    finally:
        db.close()
    # os.rename replaces atomically on POSIX; Windows requires removal first.
    if os.name == 'nt':
        os.remove(path)
    os.rename(temporary, path)
