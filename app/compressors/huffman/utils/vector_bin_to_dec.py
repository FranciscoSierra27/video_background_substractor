import math
from typing import List


class VectorBinToDecConverter:
    # Converts all values in a vector from binary to decimal numeric system
    @staticmethod
    def convert(v: List):
        t = 0
        counter = 0
        for i in range(len(v) - 1, 0, -1):
            t = t + (int(math.pow(2, counter))) * v[i]
            counter += 1
        return t
