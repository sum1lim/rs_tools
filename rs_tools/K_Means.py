from rs_tools.RGB import extract, merge
from rs_tools.utils import euclidean
import random
import re
import sys
import os
import cv2

import numpy as np
from PIL import Image, ImageFile, ImageDraw
from sklearn.cluster import KMeans

colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (255, 255, 255),
    (0, 0, 0),
]
colorNames = ["Red", "Green", "Blue", "Yellow", "Magenta", "Cyan", "White", "Black"]


def image_to_array(inImage):
    output_array = np.array([])
    for row in inImage:
        output_array = np.concatenate((output_array, row), axis=None)

    return np.array([output_array])


def generate_K_means(inFiles_li, iterations, num_classes):
    for count, inFile in enumerate(inFiles_li):
        inImage = cv2.imread(inFile, 0)
        if count == 0:
            feature_vector_matrix = image_to_array(inImage)
        else:
            feature_vector_matrix = np.append(
                feature_vector_matrix, image_to_array(inImage), axis=0
            )

    result = (
        KMeans(n_clusters=num_classes, random_state=0)
        .fit(feature_vector_matrix.T)
        .labels_
    )

    clustered_image = np.zeros(
        inImage.shape, dtype=[("x", "int"), ("y", "int"), ("z", "int")]
    )
    labeled_image = np.zeros(inImage.shape, dtype=int)

    for count, label in enumerate(result):
        row = count // clustered_image.shape[1]
        column = count - row * clustered_image.shape[1]
        clustered_image[row][column] = colors[label]
        labeled_image[row][column] = label

    return clustered_image, labeled_image
