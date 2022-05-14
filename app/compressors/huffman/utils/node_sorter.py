from typing import List


class NodeSorter:
    @staticmethod
    def sort(nodes: List):
        for i in range(len(nodes)):
            M = nodes[i]["F"]
            PM = i
            for j in range(i, len(nodes)):
                if nodes[j]["F"] > M:
                    M = nodes[j]["F"]
                    PM = j

            # Maximo
            # Intercambiamos la referncia con el maximo
            temp = nodes[i]
            nodes[i] = nodes[PM]
            nodes[PM] = temp

        return nodes
