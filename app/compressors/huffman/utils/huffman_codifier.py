from typing import List, Dict

from app.compressors.huffman.utils.custom_char import custom_chr


class HuffmanCodifier:
    @staticmethod
    def codify(buscar: str, elemento: List[Dict]):
        ruta: List = []

        while elemento[0].get("I") and elemento[0].get("D"):
            if buscar in custom_chr(elemento[0].get("I").get("C")):
                elemento[0] = elemento.copy()[0].get("I")
                ruta.append(0)
            else:
                elemento[0] = elemento.copy()[0].get("D")
                ruta.append(1)
        return ruta

