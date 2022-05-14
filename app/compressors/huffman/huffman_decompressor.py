from typing import List, Dict

import cv2
import numpy as np

from app.compressors.huffman.utils.huffman_decodifier import HuffmanTranslator


class HuffmanDecompressor:
    @staticmethod
    def decompress(rows: int, cols: int, value_tree: List[Dict], comp_background: str) -> np.ndarray:
        decompressed: str
        background_mean: List[int] = []

        routes = ''.join(format(ord(i), '08b') for i in comp_background)
        tmp_val_tree = value_tree.copy()
        background_mean = HuffmanTranslator.translate(routes, tmp_val_tree)

        np_background_mean = np.array(background_mean)
        np_background_mean = np_background_mean.reshape((rows, cols))

        #cv2.imshow("background descomprimido", np.uint8(np_background_mean))
        #cv2.waitKey(1)
        return np.uint8(np_background_mean)
