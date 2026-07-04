"""
Build erfan.exe and the Windows installer (maintainer-only).

Bundles erfan_runtime.exe so end users can run `erfan runbuild`
without installing Python or PyInstaller.
"""

import os
import shutil
import subprocess
import sys


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "compiler", "assets")
RUNTIME = os.path.join(ASSETS, "erfan_runtime.exe")
DIST = os.path.join(ROOT, "dist")
INSTALLER_DIST = os.path.join(DIST, "installer")


def run(cmd, **kwargs):
    print("+", " ".join(cmd))
    result = subprocess.run(cmd, cwd=ROOT, **kwargs)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def ensure_runtime():
    if not os.path.exists(RUNTIME):
        run([sys.executable, os.path.join(ROOT, "scripts", "build_runtime.py")])


def build_erfan_exe():
    ensure_runtime()
    os.makedirs(DIST, exist_ok=True)

    run(
        [
            sys.executable,
            "-m",
            "PyInstaller",
            "--onefile",
            "--noconfirm",
            "--clean",
            "--name",
            "erfan",
            "--distpath",
            DIST,
            "--workpath",
            os.path.join(ROOT, "build", "erfan_work"),
            "--specpath",
            os.path.join(ROOT, "build", "erfan_spec"),
            "--paths",
            ROOT,
            "--add-binary",
            f"{RUNTIME};.",
            "--hidden-import=lexer.lexer",
            "--hidden-import=lexer.token",
            "--hidden-import=lexer.keywords",
            "--hidden-import=parser.parser",
            "--hidden-import=erfan_ast.nodes",
            "--hidden-import=interpreter.interpreter",
            "--hidden-import=interpreter.environment",
            "--hidden-import=interpreter.builtin",
            "--hidden-import=interpreter.objects",
            "--hidden-import=compiler.compiler",
            "--hidden-import=compiler.packer",
            "--hidden-import=compiler.runtime",
            os.path.join(ROOT, "erfan.py"),
        ]
    )


def build_installer():
    ensure_runtime()
    os.makedirs(INSTALLER_DIST, exist_ok=True)

    erfan_exe = os.path.join(DIST, "erfan.exe")
    if not os.path.exists(erfan_exe):
        build_erfan_exe()

    staged_erfan = os.path.join(INSTALLER_DIST, "erfan.exe")
    shutil.copy2(erfan_exe, staged_erfan)

    run(
        [
            sys.executable,
            "-m",
            "PyInstaller",
            "--onefile",
            "--noconfirm",
            "--clean",
            "--windowed",
            "--name",
            "setup",
            "--distpath",
            DIST,
            "--workpath",
            os.path.join(ROOT, "build", "setup_work"),
            "--specpath",
            os.path.join(ROOT, "build", "setup_spec"),
            "--add-binary",
            f"{staged_erfan};.",
            os.path.join(ROOT, "installer", "setup.py"),
        ]
    )


def main():
    build_erfan_exe()
    build_installer()
    print(f"erfan.exe: {os.path.join(DIST, 'erfan.exe')}")
    print(f"setup.exe: {os.path.join(DIST, 'setup.exe')}")


if __name__ == "__main__":
    main()
