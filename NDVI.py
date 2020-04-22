from RGB import extract, merge
import sys
import re
import RSreq
import os
RSreq.install()
import numpy
from PIL import Image, ImageFile, ImageDraw

def NDVI(NIR, VIS):
    if(NIR+VIS != 0):
        val = (NIR - VIS)/(NIR + VIS)
        if(val<0):
            val = 0
        return val*256
    else:
        return 0

def main():

    inDir = input("Please provide bands collection path: ")

    NIR = input("Please provide the NIR band image file(Ex. B08): ")
    VIS = input("Please provide the visible band image file(Ex. B02): ")

    try:
        flist = os.listdir(inDir)
        extension = ""
        for f in flist:
            if NIR in f:
                extension = "."+f.split(".")[-1]
            elif VIS in f:
                extension = "."+f.split(".")[-1]
        if(extension == ""):
            print("The given file path is not valid or does not exist", file = sys.stderr)
            exit(1)

    except FileNotFoundError:
        print("The given file path is not valid or does not exist", file = sys.stderr)
        exit(1)

    try:
        NIR_dict = extract(inDir +"/"+ NIR + extension)
        VIS_dict = extract(inDir +"/"+ VIS + extension)
    except:
        print("The given file path is not valid or does not exist", file = sys.stderr)
        exit(1)


    NIR_list = NIR_dict["R"]
    VIS_list = VIS_dict["G"]

    NDVI_list = NIR_list[:]

    i = 0
    while(i<len(NDVI_list)):
        j = 0
        while(j<len(NDVI_list[i])):
            NDVI_list[i][j] = NDVI(NIR_list[i][j][0], VIS_list[i][j][0])
            j += 1
        i+=1

    while(True):
        outExtension = "." + input("Please provide the output file type(Ex. png, jpg, tiff): ")
        outputFile = re.sub("$", "_NDVI"+outExtension, inDir)
        
        try:
            RSreq.output(outputFile, NDVI_list)
            break
        except ValueError:
            print("Not a valid file type")


if __name__ == "__main__":
    main()