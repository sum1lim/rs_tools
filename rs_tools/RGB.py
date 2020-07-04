import sys
import re
from rs_tools.utils import install, output

install()
import numpy
import os
from PIL import Image, ImageFile, ImageDraw

ImageFile.LOAD_TRUNCATED_IMAGES = True


def extract(inFile):
    mask = 0
    if re.search("\w+\.jpeg$", inFile):
        mask = 255
    try:
        inImage = Image.open(inFile, "r")
    except:
        print("No such file or directory", file=sys.stderr)
        exit(1)

    size = inImage.size
    R_val = []
    G_val = []
    B_val = []
    num_rows = size[1]
    num_cols = size[0]
    for row in range(num_rows):
        R_list = []
        G_list = []
        B_list = []
        for column in range(num_cols):
            pix = inImage.getpixel((column, row))
            if type(pix) is int:
                print("3 bands required", file=sys.stderr)
                exit(3)

            R_list.append((mask ^ (pix[0]), mask ^ (pix[0]), mask ^ (pix[0])))
            G_list.append((mask ^ (pix[1]), mask ^ (pix[1]), mask ^ (pix[1])))
            B_list.append((mask ^ (pix[2]), mask ^ (pix[2]), mask ^ (pix[2])))

        R_val.append(R_list)
        G_val.append(G_list)
        B_val.append(B_list)

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

    pix_val = []
    num_rows = Rsize[1]
    num_cols = Rsize[0]
    for row in range(num_rows):
        tmp_list = []
        for column in range(num_cols):
            Rpix = Rimage.getpixel((column, row))[0]
            Gpix = Gimage.getpixel((column, row))[1]
            Bpix = Bimage.getpixel((column, row))[2]
            tmp_list.append((Rpix, Gpix, Bpix))

        pix_val.append(tmp_list)

    return pix_val
