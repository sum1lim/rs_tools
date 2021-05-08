import numpy as np
from PIL import Image
from rs_tools.utils import pix_val_list, increase_image_size_limit


def contrast(inImage):
    minValue = np.min(inImage)
    maxValue = np.max(inImage)

    data_range = maxValue - minValue

    outImage = np.int_((255 * (inImage - minValue)) / data_range)

    return outImage
