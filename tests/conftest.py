"""pytest itself imports stdlib calendar; activate the S60 facade explicitly."""

import os
import sys

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "Pys60_Simulator", "pys60Core")
    ),
)
from pys60_runtime import activate

activate()
