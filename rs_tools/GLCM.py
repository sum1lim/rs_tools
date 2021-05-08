import numpy as np
import cv2
import matplotlib.pyplot as plt
from tqdm import tqdm


def generate_GLCM(inFile, window_size):
    try:
        inImage = cv2.imread(inFile, 0)
    except:
        print("No such file or directory", file=sys.stderr)
        exit(1)

    rescaled_img = ((inImage / 255) * (window_size - 1)).astype(int)

    num_rows = rescaled_img.shape[0]
    num_cols = rescaled_img.shape[1]

    GLCM_matrices = []

    for row in tqdm(range(num_rows)):
        GLCM_row = []
        for col in range(num_cols):
            left, right, top, bottom = col - 5, col + 6, row - 5, row + 6

            if left < 0:
                left = 0
            if top < 0:
                top = 0
            if right > rescaled_img.shape[1]:
                right = rescaled_img.shape[1] + 1
            if bottom > rescaled_img.shape[0]:
                bottom = rescaled_img.shape[0] + 1

            window = rescaled_img[top:bottom, left:right]

            histogram_size = (window_size, window_size, 1, 1)
            histogram = np.zeros(histogram_size)

            for i in range(window.shape[0]):
                for j in range(window.shape[1]):
                    try:
                        histogram[window[i][j]][window[i][j + 1]][0][
                            0
                        ] += 1  # east direction
                    except IndexError:
                        None
                    try:
                        histogram[window[i][j]][window[i + 1][j]][0][
                            0
                        ] += 1  # south direction
                    except IndexError:
                        None
                    try:
                        histogram[window[i][j]][window[i + 1][j + 1]][0][
                            0
                        ] += 1  # southeast direction
                    except IndexError:
                        None
                    try:
                        histogram[window[i + 1][j]][window[i][j + 1]][0][
                            0
                        ] += 1  # southwest direction
                    except IndexError:
                        None

            GLCM_row.append(histogram)

        GLCM_matrices.append(GLCM_row)

    return GLCM_matrices
