from typing import List


class VectorCleaner:
    @staticmethod
    def clean(v: List) -> str:
        cleaned = str(v).replace(",", "").replace("[", "").replace("]", "").replace(" ", "")
        return cleaned
