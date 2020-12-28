import subprocess
import sys


def install():

    try:
        import pip
    except ImportError:
        subprocess.call(
            [sys.executable, "-m", "pip", "install", "--user", "upgrade", "pip==9.0.3"]
        )

        import pip

    try:
        import numpy
    except ImportError:
        subprocess.call(["pip", "install", "numpy"])
    finally:
        import numpy

    try:
        from PIL import Image, ImageFile, ImageDraw
    except ImportError:
        subprocess.call(["pip", "install", "Pillow"])
    finally:
        from PIL import Image, ImageFile, ImageDraw

    try:
        import cv2
    except ImportError:
        subprocess.call(["pip", "install", "opencv-python"])
    finally:
        import cv2
