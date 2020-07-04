from rs_tools.RGB import extract, merge
from rs_tools.utils import euclidean
import random
import re
import sys
import csv
import os

import numpy
from PIL import Image, ImageFile, ImageDraw

colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (0, 0, 0),
    (255, 255, 255),
]
colorNames = ["Red", "Green", "Blue", "Yellow", "Magenta", "Cyan", "Black", "White"]


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
            plots.append(((i, j), (firstCoord[i][j][0], secondCoord[i][j][0])))
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

        for k in cart_location.keys():
            B_points[k] = mean(cart_location[k])

        count += 1

    return (pix_location, cart_location)


def plot(cart_location):
    plot = []
    i = 0
    while i < 259:
        j = 0
        row = []
        row.append(colors[6])
        row.append(colors[6])
        row.append(colors[6])

        while j < 256:
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
    while i < 259:
        Y_reverse.append(plot[258 - i])
        i += 1

    plot = Y_reverse

    return plot


def stats(pix_location, pix_count, inFile):

    with open(re.sub("$", "_stats.csv", inFile), "w", newline="") as statsFile:
        writer = csv.writer(statsFile)
        writer.writerow(["class", "#pixels", "pecentage(%)"])
        for c in pix_location.keys():
            writer.writerow(
                [
                    colorNames[c],
                    len(pix_location[c]),
                    (len(pix_location[c]) / pix_count) * 100,
                ]
            )
        writer.writerow(["total", pix_count, 100])

    print("\nResult:")
    for c in pix_location.keys():
        print(
            colorNames[c]
            + ": "
            + str(len(pix_location[c]))
            + "pixels ("
            + str((len(pix_location[c]) / pix_count) * 100)
            + "%)"
        )
    print("\nTotal: " + str(pix_count) + "pixels")


def generate_K_means(inDir, NIR, VIS, extension, iterations, No_classes):
    try:
        print("NIR = " + inDir + "/" + NIR + extension)
        print("VIS = " + inDir + "/" + VIS + extension)
        NIR_dict = extract(inDir + "/" + NIR + extension)
        VIS_dict = extract(inDir + "/" + VIS + extension)
    except:
        print("The given file path is not valid or does not exist", file=sys.stderr)
        exit(1)

    K = iterations
    B = No_classes
    try:
        K = int(K)
        B = int(B)
    except ValueError:
        print("Only integer values are accepted.", file=sys.stderr)
        exit(3)
    if int(B) >= len(colors):
        print("# of classes allowed up to and including 7", file=sys.stderr)
        exit(4)

    firstCoord = NIR_dict["R"]
    secondCoord = VIS_dict["G"]

    locations = clustering(firstCoord, secondCoord, K, B)
    pix_location = locations[0]
    cart_location = locations[1]

    pix_val = firstCoord[:]
    pix_count = 0
    for c in pix_location.keys():
        for location in pix_location[c]:
            pix_val[location[0]][location[1]] = colors[c]
        pix_count += len(pix_location[c])

    plot_val = plot(cart_location)
    stats(pix_location, pix_count, inDir)

    return pix_val, plot_val
