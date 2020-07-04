from rs_tools.RGB import extract, merge
from rs_tools.RSreq import install
import sys
import re
import os

install()
import numpy
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
            NDVI_list[i][j] = NDVI(NIR_list[i][j][0], VIS_list[i][j][0])
            j += 1
        i += 1

    return NDVI_list


if __name__ == "__main__":
    main()
