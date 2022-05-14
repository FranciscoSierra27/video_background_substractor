from time import time
from typing import List

import numpy as np

from app.compressors.huffman.utils.bin_vector_cleaner import VectorCleaner
from app.compressors.huffman.utils.huffman_codifier import HuffmanCodifier, custom_chr
from app.compressors.huffman.utils.node_generator import NodeGenerator
from app.compressors.huffman.utils.node_sorter import NodeSorter

ITERATIONS = 30


class HuffmanCompressor:
    @staticmethod
    def compress(background_mean: np.ndarray) -> (str, List[map]):
        tic = time()
        # Probabilidad la vamos a sacar por la frecuencia, el histograma de cada
        # simbolo

        background_mean = background_mean.flatten()

        h = np.zeros(255)  # Codigo ASCII 8 bits

        for i, mean in enumerate(background_mean):
            car = int(np.mod(mean, 255))
            h[car] = h[car] + 1

        # Entonces h es el histograma
        # Vamos a codificar en una estructura
        # carcter/simbolo, Frec
        N = NodeGenerator.generate(h)
        nuevo = {}

        while len(N) > 1:
            N = NodeSorter.sort(N)
            # % Fusionar dos nodos
            #  nuevo.C=char(N(end-1).C), char(N(end).C);
            nuevo["C"] = custom_chr(N[-2]["C"]) + custom_chr(N[-1]["C"])

            nuevo["F"] = N[-1]["F"] + N[-2]["F"]

            nuevo["I"] = N[-2]
            nuevo["D"] = N[-1]

            N = N[:-2].copy()
            N.append(nuevo.copy())

        # keys = N[0]["C"]
        # for key in reversed(keys):
        #    character = HuffmanCodifier.codify(key, N.copy())
        #    print("key " + key + " = " + str(ord(key)) + " = " + VectorCleaner.clean(character))

        # Codificacion
        TB = []
        for i, letter in enumerate(background_mean):
            ruta = HuffmanCodifier.codify(custom_chr(int(np.mod(letter, 255))), N.copy())
            TB.extend(ruta)
            # print('Result : ' + str(int(letter)) + " = " +custom_chr(int(letter)) + " -> " + str(VectorCleaner.clean(ruta)))

        message = ""
        for i in range(0, len(TB), 8):
            path_bin = VectorCleaner.clean(TB[i:i + 8])
            path_letter = custom_chr(int(path_bin, 2))
            message += path_letter

        return message, N
