import numpy as np


class NodeGenerator:
    @staticmethod
    def generate(h: np.ndarray):
        # node_list es la lista de nodos con caracters que se usaron
        node_list = []

        node_map = {}

        for i in range(255):
            if h[i] > 0:  # Al menos el simbolo se utilizo una vez
                node_map["C"] = i
                node_map["F"] = h[i]
                node_map["I"] = []
                node_map["D"] = []
                node_list.append(node_map.copy())

        return node_list
