import sys
import re
import rs_tools.RSreq as rq
rq.install()
import numpy
import os
from PIL import Image, ImageFile, ImageDraw

ImageFile.LOAD_TRUNCATED_IMAGES = True

def extract(inFile):
    mask = 0
    if(re.search("\w+\.jpeg$", inFile)):
        mask = 255
    try:
        inImage = Image.open(inFile, 'r')
    except:
        print("No such file or directory", file=sys.stderr)
        exit(1)

    size = inImage.size
    R_val = []
    G_val = []
    B_val = []
    num_rows=size[1]
    num_cols=size[0]
    for row in range(num_rows):
        R_list = []
        G_list = []
        B_list = []
        for column in range(num_cols):
            pix = inImage.getpixel((column, row))
            if(type(pix) is int):
                print("3 bands required", file=sys.stderr)
                exit(3)

            R_list.append((mask^(pix[0]),mask^(pix[0]),mask^(pix[0])))
            G_list.append((mask^(pix[1]),mask^(pix[1]),mask^(pix[1])))
            B_list.append((mask^(pix[2]),mask^(pix[2]),mask^(pix[2])))
            
        R_val.append(R_list)
        G_val.append(G_list)
        B_val.append(B_list)

    RGB_dict ={}
    RGB_dict["R"] = R_val
    RGB_dict["G"] = G_val
    RGB_dict["B"] = B_val

    return RGB_dict




def merge(Rfile, Gfile, Bfile):
    try:
        Rimage = Image.open(Rfile, 'r')
        Gimage = Image.open(Gfile, 'r')
        Bimage = Image.open(Bfile, 'r')
    except:
        print("No such file or directory", file=sys.stderr)
        exit(1)

    Rsize = Rimage.size
    Gsize = Gimage.size
    Bsize = Bimage.size

    if(Rsize != Gsize or Rsize != Bsize):
        print("All 3 images should have same number of rows and columns", file=sys.stderr)
        exit(2)

    pix_val = []
    num_rows=Rsize[1]
    num_cols=Rsize[0]
    for row in range(num_rows):
        tmp_list = []
        for column in range(num_cols):
            Rpix = Rimage.getpixel((column, row))[0]
            Gpix = Gimage.getpixel((column, row))[1]
            Bpix = Bimage.getpixel((column, row))[2]
            #if(type(Rpix) is not int or type(Gpix) is not int or type(Bpix) is not int):
            #    print("Images files restricted to have only 1 band each", file=sys.stderr)
            #    exit(3)
            tmp_list.append((Rpix,Gpix,Bpix))

        pix_val.append(tmp_list)

    return pix_val




def main():
    flag = input("Extract(E) or Merge(M)?: ")

    if(flag.lower() == "e"):

        inFile = input("Please provide an image file path: ")

        RGB_dict = extract(inFile)

        directories = inFile.split("/")
        file_path=""
        for i in directories[:-1]:
            file_path += i
            file_path += "/"
        
        file_path += re.sub(".\w+$", "", directories[-1]) + "(extracted)/"
        try:
            os.mkdir(file_path)
        except FileExistsError:
            None

        band_name = directories[-1].split("+")
        while(True):
            outExtension = "." + input("Please provide the output file type(Ex. png, jpg, tiff): ")
    
            R_out = re.sub("$", outExtension, band_name[0])
            G_out = re.sub("$", outExtension, band_name[1])
            B_out = re.sub("\.\w+", outExtension, band_name[2])
            
            try:
                rq.output(file_path + R_out, RGB_dict["R"])
                rq.output(file_path + G_out, RGB_dict["G"])
                rq.output(file_path + B_out, RGB_dict["B"])
                break
            except ValueError:
                print("Not a valid file type")


    elif(flag.lower() ==  "m"):

        inDir = input("Please provide bands collection path: ")
        try:
            flist = os.listdir(inDir)
        except FileNotFoundError:
            print("The given file path is not valid or does not exist", file = sys.stderr)
            exit(1)

        blist = [re.sub("\.\w+$", "",f) for f in flist]

        try:
            Rband = input("Please provide an 'R' band image file(Ex. B04): ")
            Rindex = blist.index(Rband)
            Rfile = inDir + "/" + flist[Rindex]
            Gband = input("Please provide a 'G' band image file(Ex. B03): ")
            Gindex = blist.index(Gband)
            Gfile = inDir + "/" + flist[Gindex]
            Bband = input("Please provide a 'B' band image file(Ex. B02): ")
            Bindex = blist.index(Bband)
            Bfile = inDir + "/" + flist[Bindex]
        except ValueError:
            print("The band is not available")
            exit(5)    

        pix_val = merge(Rfile, Gfile, Bfile)

        
        directories = inDir.split("/")
        file_path=""
        for i in directories[:-1]:
            file_path += i
            file_path += "/"
        
        R_out = re.sub("\.\w+", "", Rfile)
        R_out = re.sub(".*/", "", R_out)
        G_out = re.sub("\.\w+", "", Gfile)
        G_out = re.sub(".*/", "", G_out)
        B_out = re.sub("\.\w+", "", Bfile)
        B_out = re.sub(".*/", "", B_out)
        
        while(True):
            outExtension = "." + input("Please provide the output file type(Ex. png, jpg, tiff): ")
            outFile = file_path + R_out + "+" + G_out + "+" + B_out + outExtension
            try:
                rq.output(outFile, pix_val)
                break
            except ValueError:
                print("Not a valid file type")

    else:
        print("Not a valid flag", file=sys.stderr)
        exit(4)


    exit(0)


if __name__ == "__main__":
    main()


