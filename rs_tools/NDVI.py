from rs_tools.RGB import extract, merge
import sys
import re
import os
import numpy as np
from PIL import Image, ImageFile, ImageDraw


def NDVI(NIR, VIS):
    if NIR + VIS != 0:
        val = (NIR - VIS) / (NIR + VIS)
        if val < 0:
            val = 0
        return val * 256
    else:
        return 0


def generate_NDVI(inDir, NIR, VIS, extension):
    try:
        NIR_dict = extract(inDir + "/" + NIR + extension)
        VIS_dict = extract(inDir + "/" + VIS + extension)
    except:
        print("The given file path is not valid or does not exist", file=sys.stderr)
        exit(1)

    NIR_list = NIR_dict["R"]
    VIS_list = VIS_dict["G"]

    NDVI_list = NIR_list[:]

    i = 0
    while i < len(NDVI_list):
        j = 0
        while j < len(NDVI_list[i]):
            NDVI_list[i][j] = NDVI(NIR_list[i][j], VIS_list[i][j])
            j += 1
        i += 1

    NDVI_list = np.int_(np.array(NDVI_list))
    return NDVI_list
