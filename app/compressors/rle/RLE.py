from typing import List

import cv2
import numpy as np
from time import time


class RLECalculator:
    def __init__(self, image: np.ndarray):
        self.mov_vector: np.ndarray = image[:, :, 0].flatten()
        self.cols = image.shape[1]
        self.rows = image.shape[0]

    def calculate_rle(self, mov: np.ndarray) -> (float, float):
        int_mov: np.ndarray = np.fix(mov)
        self.mov_vector: np.ndarray = int_mov.flatten()

        # Para hacer una matriz en un vector
        rle = []
        c = 1
        for i, element in enumerate(self.mov_vector):
            if i + 1 != self.mov_vector.size and element == self.mov_vector[i + 1]:
                c += 1
            else:
                rle.extend([c, element])
                c = 1

        rle.extend([c, self.mov_vector[-1]])

        razon_compresion_rle = len(rle) / self.mov_vector.size
        factor_compresion_rle = self.mov_vector.size / len(rle)

        return razon_compresion_rle, factor_compresion_rle, rle
