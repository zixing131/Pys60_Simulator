"""Load the macOS system framework even with Python 2's old dyld search."""
import ctypes.util
import sys

_original_find = ctypes.util.find_library


def _find_library(name):
    if sys.platform == 'darwin' and name == 'OpenGL':
        return '/System/Library/Frameworks/OpenGL.framework/OpenGL'
    return _original_find(name)


try:
    ctypes.util.find_library = _find_library
    from OpenGL import GL
finally:
    ctypes.util.find_library = _original_find
