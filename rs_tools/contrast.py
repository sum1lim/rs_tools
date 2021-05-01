import numpy as np
from PIL import Image
from rs_tools.utils import pix_val_list


def contrast(inFile):
    inImage = np.array(pix_val_list(Image.open(inFile, "r")))

    minValue = np.min(inImage)
    maxValue = np.max(inImage)

    data_range = maxValue - minValue

    outImage = np.int_((255 * (inImage - minValue)) / data_range)

    return outImage
