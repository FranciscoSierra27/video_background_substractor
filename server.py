#!/usr/bin/env python3
import pickle
import socket

import cv2
import numpy as np

from app.compressors.rle.rle_decompressor import decompress_rle

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            print("Listenning...")
            conn, addr = s.accept()
            data = []
            with conn:
                print('Connected by', addr)
                while True:
                    packet = conn.recv(4096)
                    if not packet:
                        break
                    data.append(packet)
                print("Recibí: " + str(len(b"".join(data))) + " datos")
                jsonRle = pickle.loads(b"".join(data))
                salida = decompress_rle(jsonRle["img"], jsonRle["rows"], jsonRle["cols"])
                cv2.imshow("Descompresion en servidor", np.uint8(salida))
                cv2.waitKey(1)
