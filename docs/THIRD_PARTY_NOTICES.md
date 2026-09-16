# Third-party notices

The following Python wrappers are adapted from Nokia's PyS60 1.4.5 source under the Apache License, Version 2.0:

- `Pys60_Simulator/pys60Core/contacts.py`: Copyright (c) 2006–2008 Nokia Corporation. Python 3 conversion, desktop backend, byte-string vCard input and a corrected new-contact rollback call.
- `Pys60_Simulator/pys60Core/calendar.py`: Copyright (c) 2006–2008 Nokia Corporation. Python 3 conversion, desktop backend, standard-library exports and persistence for undated todos.
- `Pys60_Simulator/pys60Core/sensor.py`: Copyright (c) 2007 Nokia Corporation. Original filter and wrapper logic, with Python 3 syntax conversion.
- `Pys60_Simulator/pys60Core/gles_utils.py`: Copyright (c) 2006 Nokia Corporation. Python 3 conversion and corrections to numeric/vector/fixed camera helpers. The incomplete upstream lens-flare implementation reports unsupported operation.

Original copyright and license headers remain in these files. The full license is in [licenses/Apache-2.0.txt](licenses/Apache-2.0.txt).

`_gles_manifest.py` lists the public names from PyS60's method and constant tables, with Khronos enum values resolved by `tools/generate_gles_manifest.py` from PyOpenGL metadata. Pillow, pygame, NumPy, PyOpenGL, python-dateutil, OpenCV and other installed dependencies retain their respective licenses; their implementations are not vendored here.
