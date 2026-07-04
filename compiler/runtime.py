import os
import sys


RUNTIME_NAME = "erfan_runtime.exe"


def _assets_dir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


def _project_assets():
    if getattr(sys, "frozen", False):
        return None

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(root, "compiler", "assets", RUNTIME_NAME)


def bundled_runtime_path():
    candidates = []

    if getattr(sys, "frozen", False):
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            candidates.append(os.path.join(meipass, RUNTIME_NAME))

        candidates.append(os.path.join(os.path.dirname(sys.executable), RUNTIME_NAME))

    project_asset = _project_assets()
    if project_asset:
        candidates.append(project_asset)

    candidates.append(os.path.join(_assets_dir(), RUNTIME_NAME))

    for path in candidates:
        if path and os.path.exists(path):
            return path

    return None


def ensure_runtime():
    runtime = bundled_runtime_path()
    if runtime is not None:
        return runtime

    install_dir = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else "compiler/assets"
    raise RuntimeError(
        f"Erfan runtime executable not found.\n"
        f"Expected '{RUNTIME_NAME}' next to erfan.exe or bundled inside it.\n"
        f"Reinstall Erfan, or run: python scripts/build_erfan.py"
    )
