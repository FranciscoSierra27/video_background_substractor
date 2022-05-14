from typing import List

import numpy as np


def decompress_rle(rle: List, rows: int, cols: int):
    decompressed_rle = []

    for i in range(0, len(rle), 2):
        for j in range(rle[i]):
            decompressed_rle.append(rle[i + 1])

    cols = cols

    total_size = len(decompressed_rle)
    rows = int(total_size / cols)

    matrix = []

    cols_index = 0

    for i in range(rows):
        matrix.append(decompressed_rle[cols_index:cols + cols_index])
        cols_index += cols

    image = np.array(matrix)
    image = np.expand_dims(image, axis=2)

    return image
