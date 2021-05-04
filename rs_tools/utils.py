import cv2
import sys
import numpy as np
from PIL import Image, ImageFile, ImageDraw
from rs_tools.install import install


def decompose_filepath(filepath):
    parent_directories = filepath.split("/")[:-1]
    indir_path = "/".join(parent_directories)
    File = filepath.split("/")[-1]
    [filename, extension] = File.split(".")

    return (indir_path, filename, extension)


def output(fileName, img_li):
    install()
    array = np.array(img_li)

    try:
        img = Image.fromarray(array)
        img.save(fileName)
    except TypeError:
        img = Image.fromarray(array.astype(np.uint8))
        img.save(fileName)
    except SystemError:
        print("tile cannot extend outside image")


def clip(image, boundaries):
    if not boundaries:
        left = input("left coordinate: ")
        right = input("right coordinate: ")
        top = input("top coordinate: ")
        bottom = input("bottom coordinate: ")
        print()
    else:
        (left, right, top, bottom) = boundaries

    clipped_image = image[int(top) : int(bottom), int(left) : int(right)]

    original_height = len(clipped_image)
    original_width = len(clipped_image[0])

    scale = 5000 / original_height

    new_height = int(original_height * scale)
    new_width = int(original_width * scale)
    dsize = (new_width, new_height)

    try:
        output = cv2.resize(clipped_image, dsize)
    except cv2.error:
        output = cv2.resize(clipped_image.astype(np.uint8), dsize)

    cv2.imshow(
        "clipped",
        output,
    )

    return clipped_image


def output_to_window(name, image, boundaries=None, flip=False):
    print(f"Image: {name}")
    if flip:
        image = np.flip(np.array(image), 1)
    else:
        image = np.array(image)

    print(f"Height: {str(len(image))}")
    print(f"Width: {str(len(image[0]))}\n")

    original_height = len(image)
    original_width = len(image[0])

    scale = 5000 / original_height

    new_height = int(original_height * scale)
    new_width = int(original_width * scale)
    dsize = (new_width, new_height)
    try:
        window_output = cv2.resize(image, dsize)
    except cv2.error:
        window_output = cv2.resize(image.astype(np.uint8), dsize)

    left = 0
    right = original_width - 1
    top = 0
    bottom = original_height - 1

    output = image[:]

    while True:
        window_name = name + "(press c to clip / e to erase / q to quit)"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.imshow(
            window_name,
            window_output,
        )

        keyboard_input = cv2.waitKey(0)

        if keyboard_input == ord("q"):
            return output

        elif keyboard_input == ord("c"):
            output = clip(image, boundaries)


def euclidean(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def pix_val_list(inImage, RGB=True, RGB_idx=0, mask=0):
    size = inImage.size
    num_rows = size[1]
    num_cols = size[0]

    if RGB:
        try:
            return [
                [
                    mask ^ (inImage.getpixel((column, row))[RGB_idx])
                    for column in range(num_cols)
                ]
                for row in range(num_rows)
            ]
        except TypeError:
            return [
                [mask ^ (inImage.getpixel((column, row))) for column in range(num_cols)]
                for row in range(num_rows)
            ]
            sys.exit()

    else:
        try:
            return [
                [mask ^ inImage.getpixel((column, row)) for column in range(num_cols)]
                for row in range(num_rows)
            ]
        except TypeError:
            return [
                [
                    mask ^ inImage.getpixel((column, row))
                    for column in range(num_cols)[0]
                ]
                for row in range(num_rows)
            ]


def convolution(image, filter):
    num_rows = len(image)
    num_cols = len(image[0])

    result = []

    for row in range(num_rows):
        row_vals = []
        for col in range(num_cols):
            upper_row = row - 1
            lower_row = row + 1
            left_col = col - 1
            right_col = col + 1

            if upper_row < 0:
                upper_row = num_rows - 1
            if left_col < 0:
                left_col = num_cols - 1
            if lower_row >= num_rows:
                lower_row = 0
            if right_col >= num_cols:
                right_col = 0

            convolved_value = (
                filter[0][0] * image[lower_row][right_col]
                + filter[0][1] * image[lower_row][col]
                + filter[0][2] * image[lower_row][left_col]
                + filter[1][0] * image[row][right_col]
                + filter[1][1] * image[row][col]
                + filter[1][2] * image[row][left_col]
                + filter[2][0] * image[upper_row][right_col]
                + filter[2][1] * image[upper_row][col]
                + filter[2][2] * image[upper_row][left_col]
            ) / 8

            if convolved_value < 0:
                convolved_value = 0
            elif convolved_value > 255:
                convolved_value = 255

            row_vals.append(convolved_value)

        result.append(row_vals)

    return result


def increase_image_size_limit(inFile_path):
    while True:
        increase_limit = input(
            "The input file exceeds the limit size. Do you want to increase the limit and continue? (y/n): "
        )
        if increase_limit == "y":
            Image.MAX_IMAGE_PIXELS = None
            inImage = Image.open(inFile_path, "r")
            return inImage
        elif increase_limit == "n":
            sys.exit()
