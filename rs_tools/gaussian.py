import sys
import numpy as np
from scipy.ndimage import gaussian_filter
from PIL import Image, ImageFile, ImageDraw
from rs_tools.utils import pix_val_list


def gaussian(inFile):
    try:
        inImage = Image.open(inFile, "r")
    except:
        print("No such file or directory", file=sys.stderr)
        exit(1)

    image = pix_val_list(inImage, RGB=False)
    image = np.array(image)
    result = gaussian_filter(image, sigma=1)

    return result
