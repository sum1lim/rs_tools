import subprocess
import sys


def pip_install(pkg):
    try:
        exec(f"import {pkg}")
    except ImportError:
        subprocess.call(["pip", "install", "numpy"])
    finally:
        exec(f"import {pkg}")


def install():

    try:
        import pip
    except ImportError:
        subprocess.call(
            [sys.executable, "-m", "pip", "install", "--user", "upgrade", "pip==9.0.3"]
        )
    finally:
        import pip

    pip_install("numpy")
    pip_install("PIL")
    pip_install("cv2")
