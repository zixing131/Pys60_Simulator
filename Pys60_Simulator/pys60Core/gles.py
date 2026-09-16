"""PyS60 GLES 1.x calls translated to desktop compatibility OpenGL.

All names come from the 1.4.5 method table. Unsupported OES entry points raise
NotImplementedError; CheckExtension reports them as unavailable.
"""

import re
import numpy as _np
from OpenGL import GL as _GL
from OpenGL.error import GLError
from _gles_manifest import CONSTANTS, METHODS, FORMATS
from _gl_backend import current as _current

globals().update(CONSTANTS)
_dtypes = {
    GL_FLOAT: "float32",
    GL_BYTE: "int8",
    GL_UNSIGNED_BYTE: "uint8",
    GL_SHORT: "int16",
    GL_UNSIGNED_SHORT: "uint16",
    GL_FIXED: "int32",
}
_suffixes = {
    "f": GL_FLOAT,
    "b": GL_BYTE,
    "ub": GL_UNSIGNED_BYTE,
    "s": GL_SHORT,
    "us": GL_UNSIGNED_SHORT,
    "x": GL_FIXED,
}


def _flat(value):
    if isinstance(value, array):
        return list(value)
    if isinstance(value, _np.ndarray):
        return value.reshape(-1).tolist()
    if isinstance(value, (bytes, bytearray)):
        return list(value)
    result = []
    for item in value:
        if isinstance(item, (list, tuple, array, _np.ndarray)):
            result.extend(_flat(item))
        else:
            result.append(item)
    return result


class array:
    def __init__(self, type, dimension, sequence):
        if type not in _dtypes:
            raise ValueError("Invalid array type specified")
        if not isinstance(dimension, int) or dimension < 1:
            raise ValueError("positive dimension required")
        self.type, self.dimension = type, dimension
        values = _flat(sequence)
        if type != GL_FLOAT and any(
            not isinstance(v, (int, _np.integer)) for v in values
        ):
            raise TypeError("integer array expected")
        self._data = _np.asarray(values, dtype=_dtypes[type])

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        value = self._data[index]
        return value.tolist() if hasattr(value, "tolist") else value

    def __setitem__(self, index, value):
        self._data[index] = value

    def __iter__(self):
        return iter(self._data.tolist())

    def __repr__(self):
        return "gles.array(%r, %r, %r)" % (self.type, self.dimension, list(self))


def _data(value, type):
    if type not in _dtypes:
        raise ValueError("invalid array type")
    result = (
        value._data
        if isinstance(value, array) and value.type == type
        else _np.asarray(_flat(value), dtype=_dtypes[type])
    )
    return _np.ascontiguousarray(result)


def _pointer(name, size, type, stride, value):
    context = _current()
    if value is None:
        context.pointers.pop(name, None)
        state = {
            "glVertexPointer": GL_VERTEX_ARRAY,
            "glColorPointer": GL_COLOR_ARRAY,
            "glNormalPointer": GL_NORMAL_ARRAY,
            "glTexCoordPointer": GL_TEXTURE_COORD_ARRAY,
        }[name]
        _GL.glDisableClientState(state)
        return
    if stride < 0:
        raise ValueError("negative stride")
    if name == "glVertexPointer" and size not in (2, 3, 4):
        raise ValueError("invalid vertex dimension")
    if name == "glColorPointer" and size != 4:
        raise ValueError("color dimension must be 4")
    if name == "glTexCoordPointer" and size not in (2, 3, 4):
        raise ValueError("invalid texture dimension")
    values = _data(value, type)
    if type == GL_FIXED:
        if stride and stride % 4:
            raise ValueError("fixed point stride must be aligned")
        values = values.astype("float32") / 65536.0
        type = GL_FLOAT
    context.pointers[name] = (values, size, stride)
    if name == "glNormalPointer":
        getattr(_GL, name)(type, stride, values)
    else:
        getattr(_GL, name)(size, type, stride, values)


def _pointer_wrapper(name, suffix):
    if suffix:

        def pointer(value):
            size = (
                value.dimension
                if isinstance(value, array)
                else (
                    len(value[0])
                    if value is not None
                    and len(value)
                    and isinstance(value[0], (list, tuple))
                    else 1
                )
            )
            return _pointer(
                name,
                3 if name == "glNormalPointer" else size,
                _suffixes[suffix],
                0,
                value,
            )

    elif name == "glNormalPointer":

        def pointer(type, stride, value):
            return _pointer(name, 3, type, stride, value)

    else:

        def pointer(size, type, stride, value):
            return _pointer(name, size, type, stride, value)

    return pointer


def _validate_draw(first, count):
    if first < 0 or count < 0:
        raise ValueError("negative draw range")
    states = {
        "glVertexPointer": GL_VERTEX_ARRAY,
        "glColorPointer": GL_COLOR_ARRAY,
        "glNormalPointer": GL_NORMAL_ARRAY,
        "glTexCoordPointer": GL_TEXTURE_COORD_ARRAY,
    }
    for name, (data, size, stride) in _current().pointers.items():
        if not _GL.glIsEnabled(states[name]):
            continue
        step = stride or size * data.itemsize
        if count and (first + count - 1) * step + size * data.itemsize > data.nbytes:
            raise ValueError("draw exceeds client array")


def glDrawArrays(mode, first, count):
    _current()
    _validate_draw(first, count)
    _GL.glDrawArrays(mode, first, count)


def glDrawElements(mode, count, type, indices):
    _current()
    if type not in (GL_UNSIGNED_BYTE, GL_UNSIGNED_SHORT):
        raise ValueError("invalid index type")
    data = _data(indices, type)
    if count < 0 or count > len(data):
        raise ValueError("invalid index count")
    if count:
        _validate_draw(0, int(data[:count].max()) + 1)
    _GL.glDrawElements(mode, count, type, data)


def glDrawElementsub(mode, indices):
    glDrawElements(mode, len(_flat(indices)), GL_UNSIGNED_BYTE, indices)


def glDrawElementsus(mode, indices):
    glDrawElements(mode, len(_flat(indices)), GL_UNSIGNED_SHORT, indices)


def _buffer_wrapper(name, suffix):
    sub = name == "glBufferSubData"

    def upload(*args):
        _current()
        if suffix:
            if sub:
                target, offset, data = args
                usage = None
            else:
                target, data, usage = args
                offset = 0
            data = _data(data, _suffixes[suffix])
            size = data.nbytes
        else:
            if sub:
                target, offset, size, data = args
                usage = None
            else:
                target, size, data, usage = args
                offset = 0
            if not isinstance(data, array):
                raise RuntimeError("Cannot determine data type")
            data = data._data
            if size < 0 or size > data.nbytes:
                raise ValueError("buffer size exceeds data")
        if sub:
            _GL.glBufferSubData(target, offset, size, data)
        else:
            _GL.glBufferData(target, size, data, usage)

    return upload


def Image2str(format, type, bitmap):
    import graphics

    if not isinstance(bitmap, graphics.Image):
        raise TypeError("Expecting a graphics.Image object")
    modes = {
        GL_RGB: "RGB",
        GL_RGBA: "RGBA",
        GL_LUMINANCE: "L",
        GL_LUMINANCE_ALPHA: "LA",
        GL_ALPHA: "L",
    }
    if format not in modes:
        raise ValueError("unsupported pixel format")
    pixels = bitmap.image.convert(modes[format])
    if type == GL_UNSIGNED_BYTE:
        return pixels.tobytes()
    rgb = _np.asarray(bitmap.image.convert("RGBA"), dtype="uint16")
    if type == GL_UNSIGNED_SHORT_5_6_5 and format == GL_RGB:
        packed = (
            ((rgb[:, :, 0] >> 3) << 11)
            | ((rgb[:, :, 1] >> 2) << 5)
            | (rgb[:, :, 2] >> 3)
        )
    elif type == GL_UNSIGNED_SHORT_4_4_4_4 and format == GL_RGBA:
        packed = (
            ((rgb[:, :, 0] >> 4) << 12)
            | ((rgb[:, :, 1] >> 4) << 8)
            | ((rgb[:, :, 2] >> 4) << 4)
            | (rgb[:, :, 3] >> 4)
        )
    elif type == GL_UNSIGNED_SHORT_5_5_5_1 and format == GL_RGBA:
        packed = (
            ((rgb[:, :, 0] >> 3) << 11)
            | ((rgb[:, :, 1] >> 3) << 6)
            | ((rgb[:, :, 2] >> 3) << 1)
            | (rgb[:, :, 3] >> 7)
        )
    else:
        raise ValueError("unsupported packed pixel format")
    return packed.astype("uint16").tobytes()


def glTexImage2DIO(target, level, format, border, type, image):
    glTexImage2D(
        target, level, format, image.size[0], image.size[1], border, format, type, image
    )


def glTexSubImage2DIO(target, level, xoffset, yoffset, format, type, image):
    glTexSubImage2D(
        target,
        level,
        xoffset,
        yoffset,
        image.size[0],
        image.size[1],
        format,
        type,
        image,
    )


def _pixels(value, width, height, format, type):
    import graphics

    if isinstance(value, graphics.Image):
        value = Image2str(format, type, value)
    if value is None:
        return None
    if isinstance(value, array):
        value = value._data.tobytes()
    if not isinstance(value, (bytes, bytearray)):
        raise TypeError("pixel bytes or Image expected")
    channels = {
        GL_RGB: 3,
        GL_RGBA: 4,
        GL_LUMINANCE: 1,
        GL_ALPHA: 1,
        GL_LUMINANCE_ALPHA: 2,
    }.get(format)
    if channels is None:
        raise ValueError("unsupported pixel format")
    bpp = channels if type == GL_UNSIGNED_BYTE else 2
    if width < 0 or height < 0 or len(value) < width * height * bpp:
        raise ValueError("insufficient pixel data")
    return bytes(value)


def glTexImage2D(
    target, level, internalformat, width, height, border, format, type, pixels
):
    _current()
    pixels = _pixels(pixels, width, height, format, type)
    align = int(_GL.glGetIntegerv(GL_UNPACK_ALIGNMENT))
    _GL.glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    try:
        _GL.glTexImage2D(
            target, level, internalformat, width, height, border, format, type, pixels
        )
    finally:
        _GL.glPixelStorei(GL_UNPACK_ALIGNMENT, align)


def glTexSubImage2D(
    target, level, xoffset, yoffset, width, height, format, type, pixels
):
    _current()
    pixels = _pixels(pixels, width, height, format, type)
    align = int(_GL.glGetIntegerv(GL_UNPACK_ALIGNMENT))
    _GL.glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    try:
        _GL.glTexSubImage2D(
            target, level, xoffset, yoffset, width, height, format, type, pixels
        )
    finally:
        _GL.glPixelStorei(GL_UNPACK_ALIGNMENT, align)


def glReadPixels(x, y, width, height, format, type):
    _current()
    if width < 0 or height < 0:
        raise ValueError("invalid size")
    align = int(_GL.glGetIntegerv(GL_PACK_ALIGNMENT))
    _GL.glPixelStorei(GL_PACK_ALIGNMENT, 1)
    try:
        result = _GL.glReadPixels(x, y, width, height, format, type)
        return result if isinstance(result, bytes) else result.tobytes()
    finally:
        _GL.glPixelStorei(GL_PACK_ALIGNMENT, align)


def _unsupported(name):
    def call(*args):
        raise NotImplementedError(
            "%s is not supported by the desktop GL backend" % name
        )

    call._unsupported = True
    return call


def CheckExtension(function):
    _current()
    if isinstance(function, bytes):
        function = function.decode("ascii")
    if not isinstance(function, str):
        raise TypeError("function name expected")
    candidate = globals().get(function)
    return bool(candidate is not None and not getattr(candidate, "_unsupported", False))


_aliases = {
    "glFrustumf": "glFrustum",
    "glOrthof": "glOrtho",
    "glClearDepthf": "glClearDepth",
    "glDepthRangef": "glDepthRange",
    "glClipPlanef": "glClipPlane",
    "glGetClipPlanef": "glGetClipPlane",
    "glGetTexEnvf": "glGetTexEnvfv",
    "glGetTexParameterf": "glGetTexParameterfv",
}
_fixed_offsets = {
    "glAlphaFuncx": 1,
    "glMultiTexCoord4x": 1,
    "glFogx": 1,
    "glFogxv": 1,
    "glLightModelx": 1,
    "glLightModelxv": 1,
    "glLightx": 2,
    "glLightxv": 2,
    "glMaterialx": 2,
    "glMaterialxv": 2,
    "glTexEnvx": 2,
    "glTexEnvxv": 2,
    "glTexParameterx": 2,
    "glClipPlanex": 1,
    "glPointParameterx": 1,
    "glPointParameterxv": 1,
}


def _generic(name):
    fixed = (name.endswith("x") or name.endswith("xv")) and not name.endswith("Matrix")
    translated = name
    if fixed:
        translated = name[:-2] + "fv" if name.endswith("xv") else name[:-1] + "f"
        translated = {
            "glAlphaFuncf": "glAlphaFunc",
            "glClearColorf": "glClearColor",
            "glLineWidthf": "glLineWidth",
            "glPointSizef": "glPointSize",
            "glPolygonOffsetf": "glPolygonOffset",
            "glSampleCoveragef": "glSampleCoverage",
            "glGetFixedv": "glGetFloatv",
        }.get(translated, translated)
    if name == "glGetFixedv":
        translated = "glGetFloatv"
        fixed = True
    translated = _aliases.get(translated, translated)
    function = getattr(_GL, translated, None)
    if function is None:
        return _unsupported(name)

    def call(*args):
        _current()
        args = list(args)
        if name in ("glGenTextures", "glGenBuffers") and (
            len(args) != 1 or args[0] < 1
        ):
            raise ValueError("Value must be positive")
        if name == "glDeleteBuffers":
            return _GL.glDeleteBuffers(len(args[0]), args[0])
        if name.startswith(("glLoadMatrix", "glMultMatrix")):
            args[0] = _flat(args[0])
            if len(args[0]) != 16:
                raise ValueError("matrix must contain 16 values")
        if fixed and not name.startswith("glGet"):
            offset = _fixed_offsets.get(name, 0)
            # Enum-valued parameters are not 16.16 numbers.
            enum_parameter = (
                (name in ("glFogx", "glFogxv") and args[0] == GL_FOG_MODE)
                or (
                    name in ("glLightModelx", "glLightModelxv")
                    and args[0] == GL_LIGHT_MODEL_TWO_SIDE
                )
                or (name.startswith("glTexEnv") and args[1] != GL_TEXTURE_ENV_COLOR)
                or (
                    name == "glTexParameterx"
                    and args[1]
                    in (
                        GL_TEXTURE_MIN_FILTER,
                        GL_TEXTURE_MAG_FILTER,
                        GL_TEXTURE_WRAP_S,
                        GL_TEXTURE_WRAP_T,
                        GL_GENERATE_MIPMAP,
                    )
                )
            )
            for i in range(offset, len(args)):
                if name == "glSampleCoveragex" and i == 1:
                    continue
                if not enum_parameter:
                    args[i] = (
                        [v / 65536.0 for v in _flat(args[i])]
                        if isinstance(args[i], (list, tuple, array, _np.ndarray))
                        else args[i] / 65536.0
                    )
        args = [v._data if isinstance(v, array) else v for v in args]
        result = function(*args)
        if name.startswith("glGet") and name != "glGetString":
            result = _np.asarray(result).reshape(-1).tolist()
            if fixed:
                result = [int(round(v * 65536)) for v in result]
            return tuple(result)
        if name.startswith("glGen"):
            return int(result) if args[0] == 1 else tuple(int(v) for v in result)
        if name.startswith("glIs"):
            return bool(result)
        if name == "glGetString":
            return result
        return None

    call.__name__ = name
    return call


for _name in METHODS:
    if _name in globals():
        continue
    if "OES" in _name:
        globals()[_name] = _unsupported(_name)
        continue
    _match = re.fullmatch(
        r"(gl(?:Vertex|Color|Normal|TexCoord)Pointer)(ub|us|b|s|f|x)?", _name
    )
    if _match:
        globals()[_name] = _pointer_wrapper(_match[1], _match[2])
        continue
    _match = re.fullmatch(r"(glBuffer(?:Sub)?Data)(ub|us|b|s|f|x)?", _name)
    if _match:
        globals()[_name] = _buffer_wrapper(_match[1], _match[2])
        continue
    globals()[_name] = _generic(_name)
__all__ = list(CONSTANTS) + METHODS + ["GLError"]
