"""Desktop-only device controls. S60 applications use the usual public APIs.

No phone numbers are dialled and no messages are transmitted to a real network.
Camera access occurs only after explicitly selecting an integer device index.
"""

import copy
import time
import _device
from _compat import string_types


def set_camera_source(source):
    """PIL Image, image filename/list, video filename, callable, camera index, or None."""
    import camera

    camera.release()
    if isinstance(source, (list, tuple)) and not source:
        raise ValueError("empty camera sequence")
    _device.camera_source = source
    camera._frame_index = 0


def set_gsm_location(mcc=None, mnc=None, lac=None, cellid=None):
    if mcc is None:
        _device.gsm = None
        return
    values = (mcc, mnc, lac, cellid)
    if any(not isinstance(v, int) or v < 0 for v in values):
        raise ValueError("nonnegative GSM integers expected")
    _device.gsm = values


def set_position(
    latitude,
    longitude,
    altitude=0.0,
    horizontal_accuracy=0.0,
    vertical_accuracy=0.0,
    course=None,
    satellites=None,
    timestamp=None,
):
    latitude, longitude = float(latitude), float(longitude)
    if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
        raise ValueError("invalid coordinates")
    nan = float("nan")
    course_data = dict(speed=nan, heading=nan, speed_accuracy=nan, heading_accuracy=nan)
    satellite_data = dict(
        satellites=0,
        used_satellites=0,
        time=time.time(),
        horizontal_dop=nan,
        vertical_dop=nan,
        time_dop=nan,
    )
    if course is not None:
        course_data.update(course)
    if satellites is not None:
        satellite_data.update(satellites)
    _device.position_fix = copy.deepcopy(
        dict(
            position=dict(
                latitude=latitude,
                longitude=longitude,
                altitude=float(altitude),
                horizontal_accuracy=float(horizontal_accuracy),
                vertical_accuracy=float(vertical_accuracy),
            ),
            course=course_data,
            satellites=satellite_data,
            time=time.time() if timestamp is None else float(timestamp),
        )
    )


def clear_position():
    _device.position_fix = None


def receive_sms(number, text, timestamp=None):
    import inbox

    return inbox._receive(number, text, timestamp)


def receive_call(number):
    import telephone

    telephone._receive(number)


def emit_sensor(sensor_id, data_1, data_2=0, data_3=0):
    import _sensor

    _sensor._emit(sensor_id, data_1, data_2, data_3)


def configure_sensors(definitions):
    for name, definition in definitions.items():
        if (
            not isinstance(name, string_types)
            or set(definition) != set(("id", "category"))
            or any(not isinstance(v, int) for v in definition.values())
        ):
            raise ValueError("invalid sensor definition")
    _device.sensor_definitions = copy.deepcopy(definitions)
