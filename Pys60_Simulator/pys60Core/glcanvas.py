"""PyS60 GLCanvas presented through the same framebuffer as appuifw.Canvas."""

import appuifw
import graphics
from _gles_manifest import EGL_CONSTANTS
from _gl_backend import Context

globals().update(EGL_CONSTANTS)


class GLCanvas(appuifw.Canvas):
    def __init__(
        self,
        redraw_callback,
        event_callback=None,
        resize_callback=None,
        attributes=None,
    ):
        for cb in (redraw_callback, event_callback, resize_callback):
            appuifw._callable(cb)
        if attributes is not None and (
            not isinstance(attributes, dict)
            or any(
                not isinstance(k, int) or not isinstance(v, int)
                for k, v in attributes.items()
            )
        ):
            raise TypeError("attributes must be an integer dictionary")
        allowed = {
            EGL_BUFFER_SIZE: 32,
            EGL_DEPTH_SIZE: 24,
            EGL_STENCIL_SIZE: 8,
            EGL_RED_SIZE: 8,
            EGL_GREEN_SIZE: 8,
            EGL_BLUE_SIZE: 8,
            EGL_ALPHA_SIZE: 8,
            EGL_SAMPLES: 0,
            EGL_SAMPLE_BUFFERS: 0,
        }
        for key, value in (attributes or {}).items():
            if key not in allowed or value < 0 or value > allowed[key]:
                raise ValueError("unsupported EGL framebuffer attribute")
        self._frame = 0
        self._drawing = False
        self._context = None
        super().__init__(redraw_callback, event_callback, resize_callback)
        self._mode = "RGB"
        self._context = Context(self.size, attributes or {})

    def makeCurrent(self):
        self._context.make_current()

    def drawNow(self):
        if self._drawing:
            return
        self._drawing = True
        try:
            self.makeCurrent()
            if self.redraw_callback is not None:
                self.redraw_callback(self._frame)
            self._frame += 1
            self.image = self._context.pixels()
            self.blitSelf()
        finally:
            self._drawing = False

    def redraw(self, rect=None):
        self.drawNow()

    def _resize(self, size):
        if self.size == size:
            return
        self._context.resize(size)
        self.image = graphics.PILImage.new("RGB", size)
        if self._widget is not None:
            self._widget.configure(width=size[0], height=size[1])
        if self.resize_callback is not None:
            self.resize_callback(None)
        self.drawNow()
