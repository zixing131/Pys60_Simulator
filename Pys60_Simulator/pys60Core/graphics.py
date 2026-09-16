# -*- coding: utf-8 -*-
"""Pillow backend for the PyS60 1.4.5 graphics API.

The C++ argument order (not the inconsistent blit documentation) is used.
RGB12/RGB16 and grayscale conversion follow the SDK TRgb integer formulas.
"""
import math
import numbers
import os
from PIL import Image as PILImage, ImageDraw, ImageFont, ImageChops
import e32

screen = (240, 320)
app = None
FLIP_LEFT_RIGHT, FLIP_TOP_BOTTOM, ROTATE_90, ROTATE_180, ROTATE_270 = range(1, 6)
FONT_BOLD, FONT_ITALIC, FONT_SUBSCRIPT, FONT_SUPERSCRIPT = 1, 2, 4, 8
FONT_ANTIALIAS, FONT_NO_ANTIALIAS = 16, 32
_MODES = {'1': '1', 'L': 'L', 'RGB12': 'RGB', 'RGB16': 'RGB', 'RGB': 'RGB'}
_TRANSPOSE = getattr(PILImage, 'Transpose', PILImage)
_RESAMPLE = getattr(PILImage, 'Resampling', PILImage)
try:
    string_types = (basestring,)
except NameError:
    string_types = (str,)


def _coords(coords):
    try:
        values = list(coords)
        if not values:
            raise ValueError('empty coordinate sequence')
        if isinstance(values[0], numbers.Real):
            if len(values) % 2:
                raise TypeError('even number of coordinate values expected')
            values = list(zip(values[::2], values[1::2]))
        if any(len(p) != 2 or any(not isinstance(v, numbers.Real) for v in p) for p in values):
            raise TypeError('invalid coordinate sequence')
        return [(int(p[0]), int(p[1])) for p in values]
    except (ValueError, TypeError):
        raise TypeError('invalid coordinate sequence')


def _size(size):
    points = _coords(size)
    if len(points) != 1 or min(points[0]) <= 0:
        raise ValueError('size must contain two positive values')
    return points[0]


def hex2rgb(color):
    return [(color >> 16) & 255, (color >> 8) & 255, color & 255]


def rgb2hex(color):
    r, g, b = color
    return (r << 16) | (g << 8) | b


def _rgb(color):
    if isinstance(color, numbers.Integral):
        return tuple(hex2rgb(color))
    if isinstance(color, tuple) and len(color) == 3:
        if all(isinstance(v, numbers.Integral) for v in color):
            return tuple(v & 255 for v in color)
    raise ValueError('invalid color specification; expected int or (r,g,b) tuple')


def RGB_to_Hex(color):
    return '#%02x%02x%02x' % _rgb(color)


def convertColor(color):
    return RGB_to_Hex(color)


_font_cache = {}
_FONT_SIZES = {'normal': 18, 'dense': 14, 'title': 20, 'annotation': 12,
               'legend': 14, 'symbol': 18, 'large': 22}


def _font_flags(font):
    return (font[2] or 0) if isinstance(font, (tuple, list)) and len(font) == 3 else 0


def GetFont(fill=None, font=None):
    name, size, flags = None, None, 0
    if isinstance(font, (tuple, list)):
        if not 1 <= len(font) <= 3:
            raise ValueError('font must contain one to three items')
        name = font[0]
        if len(font) > 1:
            size = font[1]
        flags = _font_flags(font)
    else:
        name = font
    if name is not None and not isinstance(name, string_types):
        raise ValueError('invalid font name')
    if size is not None and not isinstance(size, numbers.Real):
        raise TypeError('font size must be a number or None')
    if not isinstance(flags, numbers.Integral):
        raise TypeError('font flags must be integers or None')
    if flags & ~63:
        raise ValueError('invalid font flags')
    # Six points at the simulator's 96 dpi; system labels use the device profile.
    size = int(size) if size is not None else _FONT_SIZES.get(name, 8)
    if size <= 0:
        raise ValueError('font size must be positive')
    if flags & (FONT_SUBSCRIPT | FONT_SUPERSCRIPT):
        size = max(1, size * 2 // 3)
    path = os.environ.get('PYS60_FONT', os.path.join(os.path.dirname(__file__), 'fonts', 'S60SC.ttf'))
    key = (path, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]


def _metrics(text, font):
    if not text:
        return (0, 0, 0, 0), 0
    try:
        box = font.getbbox(text, anchor='ls')
        advance = int(round(font.getlength(text)))
    except AttributeError:  # Pillow for Python 2
        width, height = font.getsize(text)
        left, top = font.getoffset(text)
        ascent = font.getmetrics()[0]
        box, advance = (left, top-ascent, width, height-ascent), width
    return tuple(box), advance


def getTextFontWidth(text, size=18):
    box, advance = _metrics(text, GetFont(font=('dense', size)))
    return [advance, box[3] - box[1]]


def _convert_pixels(pixels, mode):
    """SDK GDI.INL TRgb::_Color4K/_Color64K/_Gray256, without dithering."""
    if mode in ('1', 'L'):
        if pixels.mode not in ('1', 'L'):
            import numpy as np
            rgb = np.asarray(pixels.convert('RGB'), dtype=np.uint16)
            grey = ((2 * rgb[:, :, 0] + 5 * rgb[:, :, 1] + rgb[:, :, 2]) >> 3).astype('uint8')
            pixels = PILImage.fromarray(grey)
        if mode == '1':
            return pixels.convert('L').point(lambda v: 255 if v >= 128 else 0, '1')
        return pixels.convert('L')
    pixels = pixels.convert('RGB')
    if mode == 'RGB12':
        table = [(v >> 4) * 17 for v in range(256)]
        return pixels.point(table * 3)
    if mode == 'RGB16':
        rb = [(v & 248) + ((v & 248) >> 5) for v in range(256)]
        green = [(v & 252) + ((v & 252) >> 6) for v in range(256)]
        return pixels.point(rb + green + rb)
    return pixels


class Image(object):
    def __init__(self, size, mode='RGB16', canvas=None):
        if mode is None:  # legacy simulator constructor
            mode = 'RGB16'
        if mode not in _MODES:
            raise ValueError('invalid mode')
        self._mode = mode
        self.image = PILImage.new(_MODES[mode], _size(size), 'white')
        self.canvas = canvas
        self._twipsize = tuple(v * 15 for v in self.size)
        self._pending = None
        self._waiting = False

    size = property(lambda self: self.image.size)
    mode = property(lambda self: self._mode)
    twipsize = property(lambda self: self._twipsize,
                        lambda self, value: setattr(self, '_twipsize', _coords(value)[0]))

    @staticmethod
    def new(size, mode='RGB16'):
        if mode not in _MODES:
            raise ValueError('invalid mode')
        return Image(size, mode)

    @staticmethod
    def open(filename):
        try:
            with PILImage.open(filename) as source:
                result = Image(source.size)
                result.image = _convert_pixels(source, result.mode)
                return result
        except (OSError, IOError) as exc:
            raise e32.SymbianError(-1, str(exc))

    @staticmethod
    def inspect(filename):
        with PILImage.open(filename) as source:
            return {'size': source.size}

    @staticmethod
    def from_cfbsbitmap(bitmap):
        raise e32.SymbianError(-5, 'Native CFbsBitmap handles are not available on desktop')

    @staticmethod
    def from_icon(filename, image_id, size):
        raise e32.SymbianError(-5, 'Symbian MBM/MIF icon decoding is not available')

    def _drawapi(self):
        return self

    def _bitmapapi(self):
        return self

    def _wait(self):
        if self._pending is not None:
            if self._waiting:
                raise RuntimeError('Image object busy.')
            self._waiting = True
            try:
                e32._wait_until(lambda: self._pending is None)
            finally:
                self._waiting = False

    def _operation(self, operation, callback, returns_image=False):
        if callback is not None and not callable(callback):
            raise TypeError('callback must be callable')
        self._wait()
        if callback is None:
            try:
                return operation()
            except (IOError, OSError) as exc:
                raise e32.SymbianError(-2, str(exc))
        def complete():
            self._pending = None
            try:
                result = operation()
            except (IOError, OSError):
                callback(None if returns_image else -2)
            else:
                callback(result if returns_image else 0)
        self._pending = e32._schedule(0, complete)

    def stop(self):
        e32._cancel(self._pending)
        self._pending = None

    def load(self, filename, callback=None):
        self._wait()
        if self.inspect(filename)['size'] != self.size:
            raise RuntimeError("file size doesn't match image size")
        def operation():
            with PILImage.open(filename) as source:
                self.image = _convert_pixels(source, self.mode)
            self.blitSelf()
        return self._operation(operation, callback)

    def save(self, filename, callback=None, format=None, quality=75, bpp=24, compression='default'):
        if format is None:
            suffix = os.path.splitext(filename)[1].lower()
            format = {'.jpg': 'JPEG', '.jpeg': 'JPEG', '.png': 'PNG'}.get(suffix)
            if format is None:
                raise ValueError('unrecognized suffix and format not specified')
        if format not in ('JPEG', 'PNG'):
            raise ValueError('invalid format')
        if format == 'JPEG' and not 0 <= quality <= 100:
            raise ValueError('invalid quality')
        if format == 'PNG' and bpp not in (1, 8, 24):
            raise ValueError('invalid number of bits per pixel')
        compressions = {'default': 6, 'no': 0, 'fast': 1, 'best': 9}
        if format == 'PNG' and compression not in compressions:
            raise ValueError('invalid compression level')
        def operation():
            if format == 'JPEG':
                self.image.convert('RGB').save(filename, format, quality=quality)
            else:
                mode = {1: '1', 8: 'L', 24: 'RGB'}[bpp]
                self.image.convert(mode).save(filename, format, compress_level=compressions[compression])
        return self._operation(operation, callback)

    def resize(self, size, callback=None, keepaspect=0):
        size = _size(size)
        def operation():
            actual = size
            if keepaspect:
                ratio = min(float(size[0]) / self.size[0], float(size[1]) / self.size[1])
                actual = tuple(max(1, int(v * ratio)) for v in self.size)
            result = Image(actual, self.mode)
            result.image = self.image.resize(actual, _RESAMPLE.LANCZOS if self.mode != '1' else _RESAMPLE.NEAREST)
            result._normalize()
            return result
        return self._operation(operation, callback, True)

    def transpose(self, direction, callback=None):
        directions = {FLIP_LEFT_RIGHT: _TRANSPOSE.FLIP_LEFT_RIGHT,
                      FLIP_TOP_BOTTOM: _TRANSPOSE.FLIP_TOP_BOTTOM,
                      ROTATE_90: _TRANSPOSE.ROTATE_90, ROTATE_180: _TRANSPOSE.ROTATE_180,
                      ROTATE_270: _TRANSPOSE.ROTATE_270}
        if direction not in directions:
            raise ValueError('invalid transpose direction')
        def operation():
            pixels = self.image.transpose(directions[direction])
            result = Image(pixels.size, self.mode)
            result.image = pixels
            result._normalize()
            return result
        return self._operation(operation, callback, True)

    def getpixel(self, coords):
        pixels = self.image.convert('RGB')
        return [pixels.getpixel(p) for p in _coords(coords)]

    def _color(self, value):
        if value is None:
            return None
        rgb = _rgb(value)
        if self.image.mode in ('1', 'L'):
            grey = (2 * rgb[0] + 5 * rgb[1] + rgb[2]) >> 3
            return (255 if grey >= 128 else 0) if self.image.mode == '1' else grey
        return rgb

    def clear(self, color=0xffffff):
        self.image.paste(self._color(color), (0, 0) + self.size)
        self.blitSelf()

    def _shape(self, name, coords, outline, fill, width, pattern, angles=None):
        points = _coords(coords)
        if not isinstance(width, numbers.Integral):
            raise TypeError('width must be an integer')
        outline, fill = self._color(outline), self._color(fill)
        if pattern is not None:
            if not isinstance(pattern, Image):
                raise TypeError('pattern must be an Image')
            if pattern.mode != '1':
                raise ValueError('pattern must be a binary (1-bit) Image')
        draw = ImageDraw.Draw(self.image)
        if name == 'line':
            if outline is not None and width > 0:
                draw.line(points, fill=outline, width=width)
        elif name == 'point':
            # The actual 1.4.5 C++ implementation plots only the first point.
            if outline is not None and width > 0:
                x, y = points[0]
                if width == 1:
                    draw.point((x, y), fill=outline)
                else:
                    radius = width // 2
                    draw.ellipse((x-radius, y-radius, x-radius+width-1, y-radius+width-1), fill=outline)
        else:
            if name == 'polygon':
                shapes = [points]
            else:
                if len(points) % 2:
                    raise ValueError('even number of coordinates expected')
                shapes = [(points[i][0], points[i][1], points[i+1][0]-1, points[i+1][1]-1)
                          for i in range(0, len(points), 2)]
            for shape in shapes:
                if name != 'polygon' and (shape[2] < shape[0] or shape[3] < shape[1]):
                    continue
                kwargs = {'outline': outline, 'fill': fill}
                if angles is not None:
                    kwargs.update(start=-math.degrees(angles[1]), end=-math.degrees(angles[0]))
                if name == 'arc':
                    if outline is None or width <= 0:
                        continue
                    kwargs = {'fill': outline, 'start': kwargs['start'], 'end': kwargs['end']}
                if width > 0:
                    kwargs['width'] = width
                else:
                    kwargs['outline' if name != 'arc' else 'fill'] = None
                if pattern is not None and name != 'arc':
                    mask = PILImage.new('L', self.size)
                    mask_draw = ImageDraw.Draw(mask)
                    mask_args = {'fill': 255}
                    if angles is not None:
                        mask_args.update(start=kwargs['start'], end=kwargs['end'])
                    getattr(mask_draw, name)(shape, **mask_args)
                    tile = PILImage.new('L', self.size)
                    for y in range(0, self.size[1], pattern.size[1]):
                        for x in range(0, self.size[0], pattern.size[0]):
                            tile.paste(pattern.image.convert('L'), (x, y))
                    if fill is not None:
                        self.image.paste(fill, (0, 0) + self.size, ImageChops.multiply(mask, tile))
                    kwargs['fill'] = None
                if kwargs.get('outline') is None and kwargs.get('fill') is None:
                    continue
                if name == 'polygon':
                    # Pillow 6 has no polygon width argument. Drawing the
                    # closed outline as a polyline also matches a GDI pen.
                    kwargs.pop('width', None)
                    draw.polygon(shape, **kwargs)
                    if outline is not None and width > 1:
                        draw.line(shape + [shape[0]], fill=outline, width=width)
                else:
                    getattr(draw, name)(shape, **kwargs)
                if name == 'arc' and width == 1:
                    # Pillow 6 omits the final pixel of a quadrant arc.
                    cx, cy = (shape[0]+shape[2])/2.0, (shape[1]+shape[3])/2.0
                    rx, ry = (shape[2]-shape[0])/2.0, (shape[3]-shape[1])/2.0
                    for angle in angles:
                        draw.point((int(round(cx+rx*math.cos(angle))),
                                    int(round(cy-ry*math.sin(angle)))), fill=outline)
        self.blitSelf()

    def rectangle(self, coords, outline=None, fill=None, width=1, pattern=None):
        self._shape('rectangle', coords, outline, fill, width, pattern)

    def ellipse(self, coords, outline=None, fill=None, width=1, pattern=None):
        self._shape('ellipse', coords, outline, fill, width, pattern)

    def line(self, coords, outline=None, fill=None, width=1, pattern=None):
        self._shape('line', coords, outline, fill, width, pattern)

    def polygon(self, coords, outline=None, fill=None, width=1, pattern=None):
        self._shape('polygon', coords, outline, fill, width, pattern)

    def point(self, coords, outline=None, fill=None, width=1, pattern=None):
        self._shape('point', coords, outline, fill, width, pattern)

    def arc(self, coords, start, end, outline=None, fill=None, width=1, pattern=None):
        self._shape('arc', coords, outline, fill, width, pattern, (start, end))

    def pieslice(self, coords, start, end, outline=None, fill=None, width=1, pattern=None):
        self._shape('pieslice', coords, outline, fill, width, pattern, (start, end))

    def blit(self, image, source=None, target=None, scale=0, mask=None):
        if not isinstance(image, Image):
            raise TypeError('Image object expected as 1st argument')
        if mask is not None:
            if not isinstance(mask, Image):
                raise TypeError('Mask must be an Image object')
            if mask.mode not in ('1', 'L'):
                raise ValueError('Mask must be a binary (1-bit) or grayscale (8-bit) Image')
            if mask.size != image.size:
                raise ValueError('mask and source sizes must match')
            if scale:
                raise ValueError('sorry, scaling and masking is not supported at the same time.')
        def rect(spec, size):
            points = [(0, 0)] if spec is None else _coords(spec)
            if len(points) not in (1, 2):
                raise TypeError('invalid rectangle specification')
            return points[0] + (points[1] if len(points) == 2 else size)
        sx, sy, ex, ey = rect(source, image.size)
        tx, ty, rx, ry = rect(target, self.size)
        if ex <= sx or ey <= sy:
            return
        if scale:
            if rx <= tx or ry <= ty:
                return
            pixels = image.image.crop((sx, sy, ex, ey)).resize((rx-tx, ry-ty))
            self.image.paste(_convert_pixels(pixels, self.mode), (tx, ty))
        else:
            # BitBlt clips to source bounds, without introducing black padding.
            left, top = max(0, sx), max(0, sy)
            right, bottom = min(ex, image.size[0]), min(ey, image.size[1])
            if right <= left or bottom <= top:
                return
            crop = (left, top, right, bottom)
            pixels = _convert_pixels(image.image.crop(crop), self.mode)
            alpha = mask.image.crop(crop) if mask is not None else None
            self.image.paste(pixels, (tx+left-sx, ty+top-sy), alpha)
        self.blitSelf()

    def text(self, coords, text, fill=0, font=None):
        face = GetFont(font=font)
        flags = _font_flags(font)
        stroke = 1 if flags & FONT_BOLD else 0
        mask = PILImage.new('L', self.size)
        for x, y in _coords(coords):
            glyphs = PILImage.new('L', self.size)
            draw = ImageDraw.Draw(glyphs)
            # Ask FreeType for hinted monochrome glyphs. Thresholding an
            # antialiased mask loses thin CJK strokes at small point sizes.
            monochrome = bool(flags & FONT_NO_ANTIALIAS or not flags & FONT_ANTIALIAS)
            draw.fontmode = '1' if monochrome else 'L'
            if flags & FONT_SUPERSCRIPT:
                y -= face.size // 2
            elif flags & FONT_SUBSCRIPT:
                y += face.size // 3
            # Pillow < 8 silently ignores anchor='ls'. Its default origin is
            # the ascender, so explicitly convert the PyS60 baseline to it.
            draw.text((x, y-face.getmetrics()[0]), text, fill=255,
                      font=face)
            if stroke:
                # Pillow 6's stroked monochrome masks corrupt CJK glyphs.
                # Expand the finished glyph mask instead, on every backend.
                heavier = PILImage.new('L', self.size)
                heavier.paste(glyphs, (1, 0))
                glyphs = ImageChops.lighter(glyphs, heavier)
            if flags & FONT_ITALIC:
                affine = getattr(PILImage, 'Transform', PILImage).AFFINE
                glyphs = glyphs.transform(self.size, affine, (1, .25, -.25*y, 0, 1, 0), resample=_RESAMPLE.BICUBIC)
            mask = ImageChops.lighter(mask, glyphs)
        if monochrome and flags & FONT_ITALIC:
            mask = mask.point(lambda v: 255 if v >= 128 else 0)
        self.image.paste(self._color(fill), (0, 0) + self.size, mask)
        self.blitSelf()

    def measure_text(self, text, font=None, maxwidth=-1, maxadvance=-1):
        face = GetFont(font=font)
        flags = _font_flags(font)
        def metrics(value):
            box, advance = _metrics(value, face)
            if value:
                left, top, right, bottom = box
                if flags & FONT_BOLD:
                    right += 1
                if flags & FONT_ITALIC:
                    left -= int(math.ceil(bottom * .25))
                    right -= int(math.floor(top * .25))
                shift = -face.size // 2 if flags & FONT_SUPERSCRIPT else face.size // 3 if flags & FONT_SUBSCRIPT else 0
                box = (left, top+shift, right, bottom+shift)
            return box, advance
        count = len(text)
        for i in range(1, len(text)+1):
            box, advance = metrics(text[:i])
            if (maxwidth >= 0 and box[2]-box[0] > maxwidth) or (maxadvance >= 0 and advance > maxadvance):
                count = i-1
                break
        box, advance = metrics(text[:count])
        return box, advance, count

    def _normalize(self):
        self.image = _convert_pixels(self.image, self.mode)

    def blitSelf(self):
        self._normalize()
        if self.canvas is not None and self.canvas is not self:
            self.canvas.blitSelf()


def Draw(drawable):
    if not hasattr(drawable, '_drawapi'):
        raise TypeError('object does not support drawing')
    return drawable._drawapi()


def screenshot():
    result = Image(screen)
    if app is not None:
        result.image = app.getscreen().convert('RGB').copy()
    return result

__all__ = ('Draw', 'Image', 'screenshot', 'FONT_BOLD', 'FONT_ITALIC',
           'FONT_SUBSCRIPT', 'FONT_SUPERSCRIPT', 'FONT_ANTIALIAS',
           'FONT_NO_ANTIALIAS', 'FLIP_LEFT_RIGHT', 'FLIP_TOP_BOTTOM',
           'ROTATE_90', 'ROTATE_180', 'ROTATE_270')
