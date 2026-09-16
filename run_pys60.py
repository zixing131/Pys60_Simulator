"""Run a Python 3 PyS60 application with the desktop APIs installed."""

import os
import runpy
import sys


def main():
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python run_pys60.py application.py [arguments ...]")
    core = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "Pys60_Simulator", "pys60Core"
    )
    sys.path.insert(0, core)
    from pys60_runtime import activate

    activate()
    filename = os.path.abspath(sys.argv[1])
    sys.argv = sys.argv[1:]
    sys.path.insert(0, os.path.dirname(filename))
    runpy.run_path(filename, run_name="__main__")


if __name__ == "__main__":
    main()
