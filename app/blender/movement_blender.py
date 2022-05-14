import cv2
import numpy as np


class MovementBlender:
    @staticmethod
    def blend(background: np.ndarray, movement_texture: np.ndarray):
        if len(background.shape) < 3:
            background = np.expand_dims(background, axis=2)
        if len(movement_texture.shape) < 3:
            movement_texture = np.expand_dims(movement_texture, axis=2)

        _, img_binary = cv2.threshold(movement_texture, 0, 255, cv2.THRESH_BINARY_INV)
        img_binary = np.uint8(img_binary/255)
        img_binary = np.expand_dims(img_binary, axis=2)

        blended = (img_binary * background) + movement_texture

        return blended
