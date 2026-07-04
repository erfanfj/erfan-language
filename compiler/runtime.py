import os
import sys


def _assets_dir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


def bundled_runtime_path():
    if getattr(sys, "frozen", False):
        base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
        bundled = os.path.join(base, "erfan_runtime.exe")
        if os.path.exists(bundled):
            return bundled

    local = os.path.join(_assets_dir(), "erfan_runtime.exe")
    if os.path.exists(local):
        return local

    return None


def ensure_runtime():
    runtime = bundled_runtime_path()
    if runtime is not None:
        return runtime

    raise RuntimeError(
        "Erfan runtime executable not found. "
        "Rebuild the project with scripts/build_runtime.py"
    )
