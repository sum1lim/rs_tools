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


def output_to_window(name, inImage):

    scale = 800 / inImage.size[0]
    height = int(inImage.size[1] * scale)
    width = int(inImage.size[0] * scale)
    dsize = (width, height)
    output = cv2.resize(np.flip(np.array(inImage, np.uint8), 1), dsize)

    while True:
        cv2.imshow(
            name + "(press q to quit / press c to clip)",
            output,
        )

        keyboard_input = cv2.waitKey(0)
        
        if keyboard_input == ord("q"):
            return
        elif keyboard_input == ord("c"):
            output = cv2.resize(np.flip(np.array(inImage, np.uint8), 1), dsize)
            left = int(int(input("left coordinate: ")) * scale)
            top = int(int(input("top coordinate: ")) * scale)
            right = int(int(input("right coordinate: ")) * scale)
            bottom = int(int(input("bottom coordinate: ")) * scale)

            start_point = (left, top)
            end_point = (right, bottom)

            color = (255, 255, 255)

            thickness = 2
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
