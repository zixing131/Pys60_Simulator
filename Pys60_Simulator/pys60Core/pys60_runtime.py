"""Explicit activation for hosts that imported stdlib calendar before PyS60."""

import importlib.util
import os
import sys


def activate():
    directory = os.path.dirname(__file__)
    if directory not in sys.path:
        sys.path.insert(0, directory)
    import pys60Socket

    path = os.path.join(directory, "calendar.py")
    existing = sys.modules.get("calendar")
    if existing is None or os.path.realpath(
        getattr(existing, "__file__", "")
    ) != os.path.realpath(path):
        spec = importlib.util.spec_from_file_location("calendar", path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["calendar"] = module
        try:
            spec.loader.exec_module(module)
        except Exception:
            if existing is not None:
                sys.modules["calendar"] = existing
            else:
                sys.modules.pop("calendar", None)
            raise
