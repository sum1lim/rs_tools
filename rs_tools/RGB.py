import sys
import re
from rs_tools.utils import install, output, pix_val_extractor

install()
import numpy
import os
from PIL import Image, ImageFile, ImageDraw

ImageFile.LOAD_TRUNCATED_IMAGES = True

RGB_indices = {"Red": 0, "Green": 1, "Blue": 2}


def extract(inFile):
    mask = 0
    if re.search("\w+\.jpeg$", inFile):
        mask = 255
    try:
        inImage = Image.open(inFile, "r")
    except:
        print("No such file or directory", file=sys.stderr)
        exit(1)

    try:
        R_val = pix_val_extractor(inImage, RGB_idx=RGB_indices["Red"], mask=mask)
        G_val = pix_val_extractor(inImage, RGB_idx=RGB_indices["Green"], mask=mask)
        B_val = pix_val_extractor(inImage, RGB_idx=RGB_indices["Blue"], mask=mask)
    except TypeError:
        print("3 bands required", file=sys.stderr)
        sys.exit()

    RGB_dict = {}
    RGB_dict["R"] = R_val
    RGB_dict["G"] = G_val
    RGB_dict["B"] = B_val

    return RGB_dict


def merge(inDir, Rfile, Gfile, Bfile):
    try:
        Rimage = Image.open(Rfile, "r")
        Gimage = Image.open(Gfile, "r")
        Bimage = Image.open(Bfile, "r")
    except:
        print("No such file or directory", file=sys.stderr)
        exit(1)

    Rsize = Rimage.size
    Gsize = Gimage.size
    Bsize = Bimage.size

    if Rsize != Gsize or Rsize != Bsize:
        print(
            "All 3 images should have same number of rows and columns", file=sys.stderr
        )
        exit(2)

    num_rows = Rsize[1]
    num_cols = Rsize[0]

    pix_val = [
        [
            (
                Rimage.getpixel((column, row))[0],
                Gimage.getpixel((column, row))[1],
                Bimage.getpixel((column, row))[2],
            )
            for column in range(num_cols)
        ]
        for row in range(num_rows)
    ]

    return pix_val
