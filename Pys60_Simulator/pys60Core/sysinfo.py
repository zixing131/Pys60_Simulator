# -*- coding: utf-8 -*-
"""System information for the simulated S60 3.0 device.

Radio, IMEI and battery follow the original emulator's documented values.
Memory/drive figures describe the host; display metrics describe the simulator.
"""
import os
import shutil
import sys
import e32


def imei():
    return u'000000000000000'


def sw_version():
    return u'emulator'


def os_version():
    return (9, 1, 0)


def display_pixels():
    module = sys.modules.get('appuifw')
    return module.screen if module is not None else (240, 320)


def display_twips():
    return tuple(value*15 for value in display_pixels())


def battery():
    return 0


def signal_bars():
    return 0


signal = signal_bars


def signal_dbm():
    return 0


def total_ram():
    try:
        return int(os.sysconf('SC_PHYS_PAGES')*os.sysconf('SC_PAGE_SIZE'))
    except (AttributeError, ValueError, OSError):
        try:
            import psutil
            return int(psutil.virtual_memory().total)
        except ImportError:
            raise e32.SymbianError(-5, 'Host memory information unavailable')


def free_ram():
    try:
        import psutil
        return int(psutil.virtual_memory().available)
    except ImportError:
        try:
            return int(os.sysconf('SC_AVPHYS_PAGES')*os.sysconf('SC_PAGE_SIZE'))
        except (AttributeError, ValueError, OSError):
            raise e32.SymbianError(-5, 'Host free-memory information unavailable')


def total_rom():
    return 0


def max_ramdrive_size():
    return 0


def free_drivespace():
    result = {}
    for drive in e32.drive_list():
        path = drive+'\\' if os.name == 'nt' else os.path.abspath(os.sep)
        if hasattr(shutil, 'disk_usage'):
            result[drive] = int(shutil.disk_usage(path).free)
        else:
            stat = os.statvfs(path)
            result[drive] = int(stat.f_bavail*stat.f_frsize)
    return result


def ring_type():
    return 'normal'


def active_profile():
    return 'general'
