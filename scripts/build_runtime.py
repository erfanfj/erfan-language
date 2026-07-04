"""
Build the bundled Erfan runtime stub (maintainer-only).

This only needs to be run once when preparing a release, or when
interpreter/lexer/parser code changes. End users never run this script.
"""

import os
import shutil
import subprocess
import sys


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "compiler", "assets")
OUTPUT = os.path.join(ASSETS, "erfan_runtime.exe")
STUB = os.path.join(ROOT, "compiler", "runtime_stub.py")


def main():
    os.makedirs(ASSETS, exist_ok=True)

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--noconfirm",
        "--clean",
        "--name",
        "erfan_runtime",
        "--distpath",
        ASSETS,
        "--workpath",
        os.path.join(ROOT, "build", "runtime_work"),
        "--specpath",
        os.path.join(ROOT, "build", "runtime_spec"),
        "--paths",
        ROOT,
        "--hidden-import=lexer.lexer",
        "--hidden-import=lexer.token",
        "--hidden-import=lexer.keywords",
        "--hidden-import=parser.parser",
        "--hidden-import=erfan_ast.nodes",
        "--hidden-import=interpreter.interpreter",
        "--hidden-import=interpreter.environment",
        "--hidden-import=interpreter.builtin",
        "--hidden-import=interpreter.objects",
        STUB,
    ]

    print("Building erfan_runtime.exe ...")
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        raise SystemExit(result.returncode)

    built = os.path.join(ASSETS, "erfan_runtime.exe")
    if not os.path.exists(built):
        raise SystemExit("Build finished but erfan_runtime.exe was not created")

    print(f"Runtime saved to: {built}")


if __name__ == "__main__":
    main()
