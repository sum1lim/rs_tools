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


def mean(points):
    sumX = 0
    sumY = 0
    i = 0
    while i < len(points):
        sumX += points[i][0]
        sumY += points[i][1]
        i += 1

    meanX = sumX / len(points)
    meanY = sumY / len(points)

    return (meanX, meanY)


def clustering(firstCoord, secondCoord, K, B):

    plots = []
    i = 0
    while i < len(firstCoord):
        j = 0
        while j < len(firstCoord[i]):
            plots.append(((i, j), (firstCoord[i][j], secondCoord[i][j])))
            j += 1
        i += 1

    i = 0
    B_points = []
    while i < B:
        Xrand = random.randrange(1, 256)
        Yrand = random.randrange(1, 256)
        B_points.append((Xrand, Yrand))
        i += 1

    count = 0
    cart_dimension = [0, 0]
    while count < K:
        cart_location = {}
        pix_location = {}
        for p in plots:
            k = p[0]
            v = p[1]
            i = 0
            c = i
            Min = euclidean(v, B_points[0])
            while i < B:
                length = euclidean(B_points[i], v)
                if length < Min:
                    Min = length
                    c = i
                i += 1

            try:
                pix_location[c].append(k)
                cart_location[c].append(v)
            except KeyError:
                cart_location[c] = []
                pix_location[c] = []
                pix_location[c].append(k)
                cart_location[c].append(v)

            if cart_location[c][-1][0] > cart_dimension[0]:
                cart_dimension[0] = cart_location[c][-1][0]
            if cart_location[c][-1][1] > cart_dimension[1]:
                cart_dimension[1] = cart_location[c][-1][1]

        for k in cart_location.keys():
            B_points[k] = mean(cart_location[k])

        count += 1

    return (pix_location, cart_location, cart_dimension)


def plot(cart_location, cart_dimension):
    plot = []
    i = 0
    while i < cart_dimension[1] + 4:
        j = 0
        row = []
        row.append(colors[6])
        row.append(colors[6])
        row.append(colors[6])

        while j < cart_dimension[0] + 4:
            if i > 2:
                row.append(colors[7])
            else:
                row.append(colors[6])
            j += 1

        plot.append(row)
        i += 1

    for c in cart_location.keys():
        for location in cart_location[c]:
            plot[location[1] + 3][location[0] + 3] = colors[c]

    Y_reverse = []
    i = 0
    while i < len(plot):
        Y_reverse.append(plot[258 - i])
        i += 1

    plot = Y_reverse

    return plot


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
    for count, label in enumerate(result):
        row = count // clustered_image.shape[1]
        column = count - row * clustered_image.shape[1]
        clustered_image[row][column] = colors[label]

    return clustered_image

    # try:
    #     print("NIR = " + inDir + "/" + NIR + extension)
    #     print("VIS = " + inDir + "/" + VIS + extension)
    #     NIR_dict = extract(inDir + "/" + NIR + extension)
    #     VIS_dict = extract(inDir + "/" + VIS + extension)
    # except:
    #     print("The given file path is not valid or does not exist", file=sys.stderr)
    #     exit(1)

    # K = iterations
    # B = No_classes
    # try:
    #     K = int(K)
    #     B = int(B)
    # except ValueError:
    #     print("Only integer values are accepted.", file=sys.stderr)
    #     exit(3)
    # if int(B) >= len(colors):
    #     print("# of classes allowed up to and including 7", file=sys.stderr)
    #     exit(4)

    # firstCoord = NIR_dict["R"]
    # secondCoord = VIS_dict["G"]

    # (pix_location, cart_location, cart_dimension) = clustering(firstCoord, secondCoord, K, B)

    # pix_val = firstCoord[:]
    # pix_count = 0
    # for c in pix_location.keys():
    #     for location in pix_location[c]:
    #         pix_val[location[0]][location[1]] = colors[c]
    #     pix_count += len(pix_location[c])

    # plot_val = plot(cart_location, cart_dimension)

    # return pix_val, plot_val, pix_location, pix_count
