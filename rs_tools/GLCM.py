import numpy as np
import cv2
import matplotlib.pyplot as plt

from skimage.feature import greycomatrix, greycoprops
from skimage import data


def GLCM(inFile):
    try:
        inImage = cv2.imread(inFile, 0)
    except:
        print("No such file or directory", file=sys.stderr)
        exit(1)

    six_bit_img = ((inImage / 255) * 63).astype(int)

    num_rows = six_bit_img.shape[0]
    num_cols = six_bit_img.shape[1]

    GLCM_matrices = []

    for row in range(num_rows):
        GLCM_matrices.append([])
        for col in range(num_cols):
            left, right, top, bottom = col - 5, col + 6, row - 5, row + 6

            if left < 0:
                left = 0
            if top < 0:
                top = 0
            if right > six_bit_img.shape[1]:
                right = six_bit_img.shape[1] + 1
            if bottom > six_bit_img.shape[0]:
                bottom = six_bit_img.shape[0] + 1

            window = six_bit_img[top:bottom, left:right]

            histogram_size = (64, 64)
            histogram = np.zeros(histogram_size)

            for i in range(window.shape[0]):
                for j in range(window.shape[1]):
                    try:
                        histogram[window[i][j]][window[i][j + 1]] += 1  # west direction
                    except IndexError:
                        None
                    try:
                        histogram[window[i][j]][
                            window[i + 1][j]
                        ] += 1  # north direction
                    except IndexError:
                        None
                    try:
                        histogram[window[i][j]][
                            window[i + 1][j + 1]
                        ] += 1  # northwest direction
                    except IndexError:
                        None
                    try:
                        histogram[window[i + 1][j]][
                            window[i][j + 1]
                        ] += 1  # northeast direction
                    except IndexError:
                        None

    return GLCM_matrices
