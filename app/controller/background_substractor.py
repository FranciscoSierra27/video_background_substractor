import concurrent
import pickle
import time
import concurrent.futures
from pathlib import Path

import cv2
import numpy as np

from app.blender.movement_blender import MovementBlender
from app.compressors.huffman.huffman_decompressor import HuffmanDecompressor
from app.compressors.rle.RLE import RLECalculator
from app.compressors.huffman.huffman_compressor import HuffmanCompressor
from app.sockets import client_background, client_movement
from app.substractor.movement_detector import MovementDetector


def run_secuence(video_path: str, hilos: int):
    start = time.time()

    video = cv2.VideoCapture(video_path)
    _, img = video.read()
    h, w, _ = img.shape
    movement_detector = MovementDetector(img)

    threads_result = []

    frame_counter = 0
    rle_calculator = RLECalculator(img)
    frame: np.array
    image = img
    Mov, MovT, background_mean = movement_detector.detect(img)
    _, _, rle = rle_calculator.calculate_rle(MovT)
    comp_huffman, nodes = HuffmanCompressor.compress(background_mean)
    decompressed_background = HuffmanDecompressor.decompress(h, w, nodes, comp_huffman)
    # client_background.send_compressed(comp_huffman, nodes, h, w)
    # client_movement.send_compressed(rle, h, w)
    filename = video_path.replace("resources", "results").replace(".avi", "")
    Path(filename).mkdir(parents=True, exist_ok=True)

    futures = []
    # Referencia de threathing: https://www.youtube.com/watch?v=6g79qGQo2-Q
    with concurrent.futures.ProcessPoolExecutor(hilos) as pool:
        while True:
            frame_counter += 1

            ret, frame = video.read()

            if not ret:
                break

            h, w, _ = img.shape
            if frame_counter % 1 != 0:
                continue
            futures.append(
                pool.submit(run_compressors, movement_detector, rle_calculator, frame[:], frame_counter, filename))
            if frame_counter == 795:
                break


        total_frame_size = 0
        total_rle_size = 0
        for future in concurrent.futures.as_completed(futures):
            frame_size, rle_size, rle, MovT = future.result()
            total_frame_size += frame_size
            total_rle_size += rle_size
            print("thread result got")
            blended = MovementBlender.blend(decompressed_background, MovT)
            cv2.imshow("blend", blended)
            cv2.imshow("mov", MovT)
            cv2.imshow("decompressed_background", decompressed_background)
            cv2.waitKey(1)

    print(f"total rle size: {total_rle_size}")
    print(f"total frames size: {total_frame_size}")
    print(f"percentage saved {100 - (total_rle_size * 100) / total_frame_size}")

    video.release()
    cv2.destroyAllWindows()
    end = time.time()

    # with open("result.txt", "a") as file:
    #     file.write(
    #         f"Time elapsed for {video_path} with {frame_counter} frames and {hilos} threads is = {end - start}\n")
    #     file.write(f"total rle size: {total_rle_size}\n")
    #     file.write(f"total frames size: {total_frame_size}\n")
    #     file.write(f"percentage saved {100 - (total_rle_size * 100) / total_frame_size}\n")


def run_compressors(movement_detector, rle_calculator, frame, frame_counter, filename):
    print(f"Compressing frame {frame_counter}")

    h, w, _ = frame.shape
    Mov, MovT, background_mean = movement_detector.detect(frame)
    if Mov is not None and MovT is not None and background_mean is not None:
        if frame_counter % 500 == 0:
            comp_huffman, nodes = HuffmanCompressor.compress(background_mean)
            # decompressed_background = HuffmanDecompressor.decompress(h, w, nodes, comp_huffman)
            # blended = MovementBlender.blend(decompressed_background, MovT)
    _, _, rle = rle_calculator.calculate_rle(MovT)

    w, h, c = frame.shape
    frame_size = h * w
    rle_size = len(rle)
    return frame_size, rle_size, rle, MovT
