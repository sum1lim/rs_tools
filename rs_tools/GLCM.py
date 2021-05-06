import numpy as np
import cv2


def GLCM(inFile):
    try:
        inImage = cv2.imread(inFile, 0)
    except:
        print("No such file or directory", file=sys.stderr)
        exit(1)