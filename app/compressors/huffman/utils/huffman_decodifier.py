from typing import Dict, List

from app.compressors.huffman.utils.custom_char import custom_chr


class HuffmanTranslator:
    @staticmethod
    def translate(binary_str: str, node: List[Dict]) -> List:
        node_tmp = node.copy()
        decodified: List = []
        for path in binary_str:
            if int(path):
                if not len(node_tmp[0].get("D").get("D")):
                    decodified.append(node_tmp[0].get("D").get("C"))
                    node_tmp = node.copy()
                else:
                    node_tmp[0] = node_tmp.copy()[0].get("D")
            else:
                if not len(node_tmp[0].get("I").get("I")):
                    decodified.append(node_tmp[0].get("I").get("C"))
                    node_tmp = node.copy()
                else:
                    node_tmp[0] = node_tmp.copy()[0].get("I")

        return decodified



