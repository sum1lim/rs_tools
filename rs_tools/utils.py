import subprocess
import cv2
import numpy as np


def install():

    try:
        import pip
    except ImportError:
        subprocess.call(
            [sys.executable, "-m", "pip", "install", "--user", "upgrade", "pip==9.0.3"]
        )

        import pip

    try:
        import numpy
    except ImportError:
        subprocess.call(["pip", "install", "numpy"])
    finally:
        import numpy

    try:
        from PIL import Image, ImageFile, ImageDraw
    except ImportError:
        subprocess.call(["pip", "install", "Pillow"])
    finally:
        from PIL import Image, ImageFile, ImageDraw

    try:
        import cv2
    except ImportError:
        subprocess.call(["pip", "install", "cv2"])
    finally:
        import cv2


def output(fileName, img_li):
    install()
    import numpy
    from PIL import Image, ImageFile, ImageDraw

    array = numpy.array(img_li, dtype=numpy.uint8)

    img = Image.fromarray(array)
    img.save(fileName)


def output_to_window(name, array_like):
    while True:
        cv2.imshow(
            name + "(press q to quit)", np.asarray(array_like, np.uint8),
        )
        if cv2.waitKey(10) == ord("q"):
            break


def euclidean(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def pix_val_list(inImage, BlackAndWhite=False, RGB_idx=0, mask=0):
    size = inImage.size
    num_rows = size[1]
    num_cols = size[0]

    if BlackAndWhite:
        return [
            [mask ^ inImage.getpixel((column, row)) for column in range(num_cols)]
            for row in range(num_rows)
        ]

    else:
        return [
            [
                mask ^ (inImage.getpixel((column, row))[RGB_idx])
                for column in range(num_cols)
            ]
            for row in range(num_rows)
        ]


def convolution(image, filter):
    num_rows = len(image)
    num_cols = len(image[0])

    result = image[:]

    for row in range(num_rows):
        for col in range(num_cols):
            upper_row = row-1
            lower_row = row+1
            left_col = col-1
            right_col = col+1

            if upper_row < 0:
                upper_row = num_rows-1
            if left_col < 0:
                left_col = num_cols-1
            if lower_row >= num_rows:
                lower_row = 0
            if right_col >= num_cols:
                right_col = 0

            result[row][col] = (
                filter[0][0] * image[lower_row][right_col] +
                filter[0][1] * image[lower_row][col] +
                filter[0][2] * image[lower_row][left_col] +
                filter[1][0] * image[row][right_col] +
                filter[1][1] * image[row][col] +
                filter[1][2] * image[row][left_col] +
                filter[2][0] * image[upper_row][right_col] +
                filter[2][1] * image[upper_row][col] +
                filter[2][2] * image[upper_row][left_col]
            ) // 8

    return result