import sys
import re
from rs_tools.RSreq import install, output

install()
import numpy
import os
from PIL import Image, ImageFile, ImageDraw

ImageFile.LOAD_TRUNCATED_IMAGES = True


def extract(inFile, extension):
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

    directories = inFile.split("/")[:-1]
    infile_name = inFile.split("/")[-1]
    dir_path = "/".join(directories)

    dir_path += "/" + re.sub(".\w+$", "", infile_name) + "(extracted)"
    try:
        os.mkdir(dir_path)
    except FileExistsError:
        None

    band_names = infile_name.split("+")
    while True:
        outExtension = "." + extension

        R_out = re.sub("$", outExtension, band_names[0])
        G_out = re.sub("$", outExtension, band_names[1])
        B_out = re.sub("\.\w+", outExtension, band_names[2])

        try:
            output(os.path.join(dir_path, R_out), RGB_dict["R"])
            output(os.path.join(dir_path, G_out), RGB_dict["G"])
            output(os.path.join(dir_path, B_out), RGB_dict["B"])
            break
        except ValueError:
            print("Not a valid file type")


def merge(inDir, Rfile, Gfile, Bfile, extension):
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

    directories = inDir.split("/")
    file_path = ""
    for i in directories[:-1]:
        file_path += i
        file_path += "/"

    R_out = re.sub("\.\w+", "", Rfile)
    R_out = re.sub(".*/", "", R_out)
    G_out = re.sub("\.\w+", "", Gfile)
    G_out = re.sub(".*/", "", G_out)
    B_out = re.sub("\.\w+", "", Bfile)
    B_out = re.sub(".*/", "", B_out)

    while True:
        outExtension = "." + extension
        outFile = file_path + R_out + "+" + G_out + "+" + B_out + outExtension
        try:
            output(outFile, pix_val)
            break
        except ValueError:
            print("Not a valid file type")
