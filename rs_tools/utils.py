import cv2
import sys
import numpy as np
from PIL import Image, ImageFile, ImageDraw
from rs_tools.install import install


def output(fileName, img_li):
    install()
    array = np.array(img_li, dtype=np.uint8)

    img = Image.fromarray(array)
    img.save(fileName)


def output_to_window(name, image, boundaries=None):
    image = np.flip(np.array(image, np.uint8), 1)

    print(f"Height: {str(len(image))}")
    print(f"Width: {str(len(image[0]))}")

    original_height = len(image)
    original_width = len(image[0])

    scale = 5000 / original_height

    new_height = int(original_height * scale)
    new_width = int(original_width * scale)
    dsize = (new_width, new_height)
    output = cv2.resize(image, dsize)

    left = 0
    right = original_width - 1
    top = 0
    bottom = original_height - 1

    while True:
        window_name = name + "(press c to clip / press q to quit)"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.imshow(
            window_name,
            output,
        )

        keyboard_input = cv2.waitKey(0)

        if keyboard_input == ord("q"):
            return image[int(top) : int(bottom), int(left) : int(right)]

        elif keyboard_input == ord("c"):
            output = cv2.resize(np.flip(np.array(image, np.uint8), 1), dsize)
            if not boundaries:
                left = input("left coordinate: ")
                right = input("right coordinate: ")
                top = input("top coordinate: ")
                bottom = input("bottom coordinate: ")
            else:
                (left, right, top, bottom) = boundaries

            start_point = (int(int(left) * scale), int(int(top) * scale))
            end_point = (int(int(right) * scale), int(int(bottom) * scale))

            color = (255, 255, 255)

            thickness = 10
            output = cv2.rectangle(output, start_point, end_point, color, thickness)


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
            print("3 bands required", file=sys.stderr)
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
