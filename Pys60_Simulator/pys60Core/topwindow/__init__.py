# -*- coding: utf-8 -*-
"""TopWindow overlay for the desktop simulator.

Native window-server shadow, corner and fading effects are approximations.
"""
import appuifw
import graphics


class TopWindow(object):
    def __init__(self):
        self._position = (0, 0)
        self._size = (1, 1)
        self._background_color = 0xffffff
        self._images = []
        self._visible = False
        self._window = None
        self._label = None
        self._shadow = 0
        self._corner_type = 'square'
        self._fading = 0

    def _set_position(self, value):
        self._position = graphics._coords(value)[0]
        self._refresh()

    position = property(lambda self: self._position, _set_position)

    def _set_size(self, value):
        self._size = graphics._size(value)
        self._refresh()

    size = property(lambda self: self._size, _set_size)
    maximum_size = property(lambda self: appuifw.screen)

    def _set_background(self, value):
        graphics._rgb(value)
        self._background_color = value
        self._refresh()

    background_color = property(lambda self: self._background_color, _set_background)

    def _set_shadow(self, value):
        self._shadow = int(value)
        self._refresh()

    shadow = property(lambda self: self._shadow, _set_shadow)

    def _set_corner(self, value):
        if value not in ('square', 'corner1', 'corner2', 'corner3', 'corner5'):
            raise KeyError(value)
        self._corner_type = value
        self._refresh()

    corner_type = property(lambda self: self._corner_type, _set_corner)
    fading = property(lambda self: self._fading, lambda self, value: setattr(self, '_fading', int(value)))

    @staticmethod
    def _rect(image, position):
        if not isinstance(image, graphics.Image):
            raise TypeError('Image expected')
        if len(position) == 2:
            x, y = position
            return (x, y, x+image.size[0], y+image.size[1])
        if len(position) == 4:
            return tuple(position)
        raise TypeError('position must contain 2 or 4 integer values')

    def add_image(self, image, position):
        self._images.append((image, self._rect(image, position)))
        self._refresh()

    def remove_image(self, image, position=None):
        rect = None if position is None else self._rect(image, position)
        keep = [(img, pos) for img, pos in self._images if not (img is image and (rect is None or pos == rect))]
        if len(keep) == len(self._images):
            raise ValueError('no such image')
        self._images = keep
        self._refresh()

    def _set_images(self, items):
        values = [(img, self._rect(img, pos)) for img, pos in items]
        self._images = values
        self._refresh()

    images = property(lambda self: list(self._images), _set_images)

    def _set_visible(self, value):
        if value:
            self.show()
        else:
            self.hide()

    visible = property(lambda self: int(self._visible), _set_visible)

    def show(self):
        self._visible = True
        if self not in appuifw.app._overlays:
            appuifw.app._overlays.append(self)
        self._refresh()

    def hide(self):
        self._visible = False
        if self in appuifw.app._overlays:
            appuifw.app._overlays.remove(self)
        if self._window is not None:
            self._window.withdraw()

    def _render(self):
        result = graphics.Image.new(self.size)
        result.clear(self.background_color)
        for image, position in self._images:
            result.blit(image, target=position, scale=1)
        return result

    def _refresh(self):
        if not self._visible or appuifw._ensure_root() is None:
            return
        from PIL import ImageTk
        if self._window is None:
            self._window = appuifw.tk.Toplevel(appuifw.root)
            self._window.overrideredirect(True)
            self._window.attributes('-topmost', True)
            self._label = appuifw.tk.Label(self._window, borderwidth=0)
            self._label.pack()
        x, y = self.position
        self._window.geometry('%dx%d+%d+%d' % (self.size+(appuifw.root.winfo_rootx()+x, appuifw.root.winfo_rooty()+y)))
        self._photo = ImageTk.PhotoImage(self._render().image, master=self._window)
        self._label.configure(image=self._photo)
        self._window.deiconify()
