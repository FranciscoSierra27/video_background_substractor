#!/usr/bin/env python3
import json
import math
import pickle
import socket
from typing import List, Dict

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 60001  # The port used by the server


def build_json(huff_img: List, huff_dict: List[Dict], rows: int, cols: int) -> json:
    rle_json = {
        "rows": rows,
        "cols": cols,
        "dict": huff_dict,
        "img": huff_img
    }

    return rle_json


def send_compressed(huff_img: List, huff_dict: List[Dict], rows: int, cols: int):
    rle_bytes = pickle.dumps((build_json(huff_img, huff_dict, rows, cols)))

    bytes_index = 0
    bytes_batch = 4096

    packages_qty = math.ceil(len(rle_bytes) / bytes_batch)

    bytes_to_send = bytes_batch
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.connect((HOST, PORT))
        for i in range(packages_qty + 1):
            s.sendall(rle_bytes[bytes_index:bytes_to_send])

            bytes_index = bytes_to_send

            if bytes_batch * (i + 1) > len(rle_bytes):
                bytes_to_send = len(rle_bytes)
            else:
                bytes_to_send = bytes_batch * (i + 1)

        print("Datos enviados satisfactoriamente: " + str(bytes_to_send))
