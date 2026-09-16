"""Desktop compatibility GL contexts with an offscreen framebuffer per canvas."""

import ctypes
import ctypes.util
import os
import glob
import sys
import threading
import weakref
import e32

_current = threading.local()


class _SDLContext:
    """Separate SDL window/context pairs, never shared mutable GL state."""

    def __init__(self):
        candidates = [os.environ.get("PYS60_SDL_LIBRARY")]
        try:
            import importlib.util

            spec = importlib.util.find_spec("pygame")
            package = os.path.dirname(spec.origin) if spec is not None else ""
            candidates += glob.glob(
                os.path.join(package, "..", "pygame.libs", "*SDL2-*")
            )
            candidates += glob.glob(os.path.join(package, "SDL2.dll"))
            candidates += glob.glob(os.path.join(package, ".dylibs", "*SDL2*"))
        except ImportError:
            pass
        candidates.append(ctypes.util.find_library("SDL2"))
        self.lib = None
        for path in candidates:
            if not path:
                continue
            try:
                self.lib = ctypes.CDLL(path)
                break
            except OSError:
                continue
        if self.lib is None:
            raise e32.SymbianError(-5, "SDL2 library not found; set PYS60_SDL_LIBRARY")
        signatures = {
            "SDL_InitSubSystem": ([ctypes.c_uint], ctypes.c_int),
            "SDL_QuitSubSystem": ([ctypes.c_uint], None),
            "SDL_GL_SetAttribute": ([ctypes.c_int, ctypes.c_int], ctypes.c_int),
            "SDL_CreateWindow": (
                [
                    ctypes.c_char_p,
                    ctypes.c_int,
                    ctypes.c_int,
                    ctypes.c_int,
                    ctypes.c_int,
                    ctypes.c_uint,
                ],
                ctypes.c_void_p,
            ),
            "SDL_DestroyWindow": ([ctypes.c_void_p], None),
            "SDL_GL_CreateContext": ([ctypes.c_void_p], ctypes.c_void_p),
            "SDL_GL_DeleteContext": ([ctypes.c_void_p], None),
            "SDL_GL_MakeCurrent": ([ctypes.c_void_p, ctypes.c_void_p], ctypes.c_int),
            "SDL_GetError": ([], ctypes.c_char_p),
        }
        for name, (arguments, result) in signatures.items():
            function = getattr(self.lib, name)
            function.argtypes, function.restype = arguments, result
        if self.lib.SDL_InitSubSystem(0x20):
            raise e32.SymbianError(-5, self.lib.SDL_GetError().decode())
        self.window = self.context = None
        for attribute, value in ((17, 2), (18, 1), (21, 2), (6, 24), (7, 8)):
            self.lib.SDL_GL_SetAttribute(attribute, value)
        self.window = self.lib.SDL_CreateWindow(b"PyS60 GL", 0, 0, 1, 1, 0x2 | 0x8)
        if self.window:
            self.context = self.lib.SDL_GL_CreateContext(self.window)
        if not self.context:
            error = self.lib.SDL_GetError().decode()
            self.close()
            raise e32.SymbianError(-5, error)

    def make_current(self):
        if self.lib.SDL_GL_MakeCurrent(self.window, self.context):
            raise e32.SymbianError(-5, self.lib.SDL_GetError().decode())

    def close(self):
        if self.context:
            self.lib.SDL_GL_DeleteContext(self.context)
            self.context = None
        if self.window:
            self.lib.SDL_DestroyWindow(self.window)
            self.window = None
        self.lib.SDL_QuitSubSystem(0x20)


class Context:
    def __init__(self, size, attributes):
        self.owner = threading.current_thread().ident
        self.pointers = {}
        self.closed = False
        self.context = None
        self.sdl = None
        self.fbo = self.texture = self.depth = 0
        from _opengl import GL
        from OpenGL.GL.EXT import framebuffer_object as F

        self.GL, self.F = GL, F
        if sys.platform == "darwin" and os.environ.get("PYS60_GL_BACKEND") != "sdl":
            self.lib = ctypes.CDLL("/System/Library/Frameworks/OpenGL.framework/OpenGL")
            for name, args in [
                (
                    "CGLChoosePixelFormat",
                    [
                        ctypes.POINTER(ctypes.c_int),
                        ctypes.POINTER(ctypes.c_void_p),
                        ctypes.POINTER(ctypes.c_int),
                    ],
                ),
                (
                    "CGLCreateContext",
                    [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p)],
                ),
                ("CGLSetCurrentContext", [ctypes.c_void_p]),
                ("CGLDestroyContext", [ctypes.c_void_p]),
                ("CGLDestroyPixelFormat", [ctypes.c_void_p]),
            ]:
                getattr(self.lib, name).argtypes = args
            attrs = (ctypes.c_int * 7)(8, 24, 12, 24, 13, 8, 0)
            pixel = ctypes.c_void_p()
            count = ctypes.c_int()
            context = ctypes.c_void_p()
            if self.lib.CGLChoosePixelFormat(
                attrs, ctypes.byref(pixel), ctypes.byref(count)
            ):
                raise e32.SymbianError(-5, "cannot choose desktop GL pixel format")
            error = self.lib.CGLCreateContext(pixel, None, ctypes.byref(context))
            self.lib.CGLDestroyPixelFormat(pixel)
            if error:
                raise e32.SymbianError(-5, "cannot create desktop GL context")
            self.context = context
        else:
            self.sdl = _SDLContext()
        self.make_current()
        if not GL.glGetString(GL.GL_VERSION):
            raise e32.SymbianError(-5, "no compatibility OpenGL context")
        self.fbo = int(F.glGenFramebuffersEXT(1))
        self.texture = int(GL.glGenTextures(1))
        self.depth = int(F.glGenRenderbuffersEXT(1))
        self.resize(size)

    def make_current(self):
        if self.closed:
            raise RuntimeError("GL context is closed")
        if threading.current_thread().ident != self.owner:
            raise RuntimeError("GLCanvas belongs to another thread")
        if self.context is not None:
            self.lib.CGLSetCurrentContext(self.context)
        elif self.sdl is not None:
            self.sdl.make_current()
        if self.fbo:
            self.F.glBindFramebufferEXT(self.F.GL_FRAMEBUFFER_EXT, self.fbo)
        _current.value = weakref.ref(self)

    def resize(self, size):
        self.make_current()
        GL, F = self.GL, self.F
        old = int(GL.glGetIntegerv(GL.GL_TEXTURE_BINDING_2D))
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)
        GL.glTexImage2D(
            GL.GL_TEXTURE_2D,
            0,
            GL.GL_RGBA8,
            size[0],
            size[1],
            0,
            GL.GL_RGBA,
            GL.GL_UNSIGNED_BYTE,
            None,
        )
        F.glBindFramebufferEXT(F.GL_FRAMEBUFFER_EXT, self.fbo)
        F.glFramebufferTexture2DEXT(
            F.GL_FRAMEBUFFER_EXT,
            F.GL_COLOR_ATTACHMENT0_EXT,
            GL.GL_TEXTURE_2D,
            self.texture,
            0,
        )
        F.glBindRenderbufferEXT(F.GL_RENDERBUFFER_EXT, self.depth)
        F.glRenderbufferStorageEXT(
            F.GL_RENDERBUFFER_EXT, 0x88F0, size[0], size[1]
        )  # DEPTH24_STENCIL8
        F.glFramebufferRenderbufferEXT(
            F.GL_FRAMEBUFFER_EXT,
            F.GL_DEPTH_ATTACHMENT_EXT,
            F.GL_RENDERBUFFER_EXT,
            self.depth,
        )
        F.glFramebufferRenderbufferEXT(
            F.GL_FRAMEBUFFER_EXT,
            F.GL_STENCIL_ATTACHMENT_EXT,
            F.GL_RENDERBUFFER_EXT,
            self.depth,
        )
        GL.glBindTexture(GL.GL_TEXTURE_2D, old)
        if (
            F.glCheckFramebufferStatusEXT(F.GL_FRAMEBUFFER_EXT)
            != F.GL_FRAMEBUFFER_COMPLETE_EXT
        ):
            raise e32.SymbianError(-5, "incomplete GL framebuffer")
        self.size = size
        GL.glViewport(0, 0, *size)

    def pixels(self):
        self.make_current()
        GL = self.GL
        from PIL import Image

        align = int(GL.glGetIntegerv(GL.GL_PACK_ALIGNMENT))
        GL.glPixelStorei(GL.GL_PACK_ALIGNMENT, 1)
        try:
            pixels = GL.glReadPixels(
                0, 0, self.size[0], self.size[1], GL.GL_RGB, GL.GL_UNSIGNED_BYTE
            )
        finally:
            GL.glPixelStorei(GL.GL_PACK_ALIGNMENT, align)
        return Image.frombytes("RGB", self.size, bytes(pixels)).transpose(
            getattr(Image, "Transpose", Image).FLIP_TOP_BOTTOM
        )

    def close(self):
        if self.closed:
            return
        self.make_current()
        if self.context is not None:
            self.lib.CGLSetCurrentContext(None)
            self.lib.CGLDestroyContext(self.context)
        elif self.sdl is not None:
            self.sdl.close()
        self.closed = True
        self.pointers.clear()

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass


def current():
    ref = getattr(_current, "value", None)
    context = ref() if ref else None
    if context is None or context.closed:
        raise RuntimeError("no current GLCanvas; call makeCurrent() first")
    return context
