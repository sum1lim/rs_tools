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
            [sys.executable, "-m", "pip", "install", "--user", "upgrade", "pip==21.1.1"]
        )
    finally:
        import pip

    pip_install("numpy", "numpy")
    pip_install("PIL", "pillow")
    pip_install("cv2", "opencv-python")
    pip_install("scipy", "scipy")
    pip_install("matplotlib", "matplotlib")
    pip_install("skimage", "scikit-image")
    pip_install("sklearn", "scikit-learn")
    pip_install("tqdm", "tqdm")
