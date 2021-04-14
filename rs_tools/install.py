import subprocess
import sys


def pip_install(import_name, pkg):
    try:
        exec(f"import {import_name}")
    except ImportError:
        subprocess.call(["pip", "install", pkg])
    finally:
        exec(f"import {import_name}")


def install():

    try:
        import pip
    except ImportError:
        subprocess.call(
            [sys.executable, "-m", "pip", "install", "--user", "upgrade", "pip==9.0.3"]
        )
    finally:
        import pip

    pip_install("numpy", "numpy")
    pip_install("pillow", "PIL")
    pip_install("opencv-python", "cv2")