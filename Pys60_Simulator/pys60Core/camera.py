"""Camera API using configured images, video files, or an OpenCV camera index."""

import io
import os
import e32
import graphics
import _device
from PIL import Image as PILImage

EOpenComplete, EPrepareComplete, ERecordComplete = 0xFA0, 0xFA1, 0xFA2
_modes = ["RGB", "RGB16", "RGB12", "JPEG_Exif", "JPEG_JFIF"]
_finder = None
_pending = None
_capture = None
_capture_source = None
_frame_index = 0
_writer = None
_record_cb = None
_record_events = []
_busy = False
_sizes = [(640, 480), (320, 240), (160, 120), (1280, 960)]


def cameras_available():
    return int(_device.camera_source is not None)


def image_modes():
    return list(_modes) if cameras_available() else []


def image_sizes(mode="RGB16"):
    if mode not in _modes:
        raise KeyError(mode)
    return list(_sizes) if cameras_available() else []


def max_zoom():
    return 4 if cameras_available() else 0


def flash_modes():
    return ["none"]


def exposure_modes():
    return ["auto"]


def white_balance_modes():
    return ["auto"]


def _frame(size):
    global _capture, _capture_source, _frame_index
    source = _device.camera_source
    if source is None:
        raise e32.SymbianError(-18, "camera source is not configured")
    if callable(source):
        pixels = source()
        if isinstance(pixels, graphics.Image):
            pixels = pixels.image
        if not isinstance(pixels, PILImage.Image):
            raise TypeError("camera source must return an image")
    elif (
        isinstance(source, (list, tuple))
        or isinstance(source, PILImage.Image)
        or (
            isinstance(source, str)
            and source.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))
        )
    ):
        item = (
            source[_frame_index % len(source)]
            if isinstance(source, (list, tuple))
            else source
        )
        _frame_index += 1
        if isinstance(item, graphics.Image):
            item = item.image
        if isinstance(item, PILImage.Image):
            pixels = item.copy()
        else:
            with PILImage.open(item) as image:
                pixels = image.convert("RGB")
    else:
        import cv2

        if _capture is None or _capture_source != source:
            if _capture is not None:
                _capture.release()
            _capture = cv2.VideoCapture(source)
            _capture_source = source
        if not _capture.isOpened():
            raise e32.SymbianError(-1, "cannot open camera source")
        ok, frame = _capture.read()
        if not ok and isinstance(source, str):
            _capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ok, frame = _capture.read()
        if not ok:
            raise e32.SymbianError(-2, "camera capture failed")
        pixels = PILImage.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    return pixels.convert("RGB").resize(size)


def take_photo(
    mode="RGB16",
    size=(640, 480),
    zoom=0,
    flash="none",
    exposure="auto",
    white_balance="auto",
    position=0,
):
    global _busy
    if position < 0 or position >= cameras_available():
        raise ValueError("Camera position not supported")
    if size not in image_sizes(mode):
        raise ValueError("Size not supported for camera")
    if not isinstance(zoom, int) or not 0 <= zoom <= max_zoom():
        raise ValueError("unsupported zoom")
    for value, allowed in (
        (flash, flash_modes()),
        (exposure, exposure_modes()),
        (white_balance, white_balance_modes()),
    ):
        if value not in allowed:
            raise ValueError("camera setting not supported by backend")
    if _busy:
        raise RuntimeError("Photo request ongoing")
    _busy = True
    try:
        pixels = _frame(size)
        if zoom:
            factor = 1 + zoom
            w, h = size
            pixels = pixels.crop(
                (
                    w // 2 - w // (2 * factor),
                    h // 2 - h // (2 * factor),
                    w // 2 + w // (2 * factor),
                    h // 2 + h // (2 * factor),
                )
            ).resize(size)
        if mode.startswith("JPEG"):
            output = io.BytesIO()
            options = {}
            if mode == "JPEG_Exif":
                exif = PILImage.Exif()
                exif[0x010F] = "PyS60 Simulator"
                options["exif"] = exif
            pixels.save(output, "JPEG", **options)
            return output.getvalue()
        result = graphics.Image.new(size, mode)
        result.image = pixels
        result.blitSelf()
        return result
    finally:
        _busy = False


def start_finder(call_back, backlight_on=1, size=None):
    global _finder, _pending
    if _finder is not None:
        raise RuntimeError("View finder is started already")
    if not callable(call_back):
        raise TypeError("callback must be callable")
    if size is None:
        import appuifw

        size = appuifw.app.layout(appuifw.EMainPane)[0]
    size = graphics._size(size)
    if not cameras_available():
        raise e32.SymbianError(-18, "camera source is not configured")
    _finder = call_back

    def tick():
        global _pending
        if _finder is not call_back:
            return
        result = graphics.Image.new(size)
        try:
            result.image = _frame(size)
            result.blitSelf()
            if _writer is not None:
                import cv2, numpy

                frame = cv2.cvtColor(
                    numpy.asarray(result.image.resize((640, 480))), cv2.COLOR_RGB2BGR
                )
                _writer.write(frame)
            if backlight_on:
                e32.reset_inactivity()
            _pending = e32._schedule(1 / 15.0, tick)
            call_back(result)
        except Exception:
            stop_finder()
            raise

    _pending = e32._schedule(0, tick)


def stop_finder():
    global _finder, _pending
    e32._cancel(_pending)
    _finder, _pending = None, None


def start_record(filename, cb):
    global _writer, _record_cb
    if _finder is None:
        raise RuntimeError("View finder is not started")
    if not callable(cb):
        raise TypeError("callback must be callable")
    if _writer is not None:
        raise RuntimeError("recording already active")
    import cv2

    extension = os.path.splitext(filename)[1].lower()
    if extension not in (".avi", ".mp4", ".mov"):
        raise e32.SymbianError(-5, "desktop recording supports AVI, MP4 and MOV")
    writer = cv2.VideoWriter(
        str(filename),
        cv2.VideoWriter_fourcc(*("MJPG" if extension == ".avi" else "mp4v")),
        15.0,
        (640, 480),
    )
    if not writer.isOpened():
        raise e32.SymbianError(-2, "cannot create recording")
    _writer, _record_cb = writer, cb
    _record_events.extend(
        [
            e32._schedule(0, lambda: cb(0, EOpenComplete)),
            e32._schedule(0.001, lambda: cb(0, EPrepareComplete)),
        ]
    )


def stop_record():
    global _writer, _record_cb
    if _writer is not None:
        _writer.release()
        callback = _record_cb
        _writer, _record_cb = None, None
        e32._schedule(0, lambda: callback(0, ERecordComplete))


def release():
    global _capture, _capture_source
    stop_record()
    stop_finder()
    if _capture is not None:
        _capture.release()
    _capture, _capture_source = None, None


def _handle():
    if not cameras_available():
        raise e32.SymbianError(-18, "camera unavailable")
    return id(_capture) if _capture is not None else id(_device.camera_source)
