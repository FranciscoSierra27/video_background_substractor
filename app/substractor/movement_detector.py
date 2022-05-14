import sys
import cv2
import numpy as np


class MovementDetector:
    def __init__(self, img):
        self.h, self.w, _ = img.shape
        self.S = 100 * np.ones((self.h, self.w))  # desviacion estandar
        self.rho = 1 - (1 / 30)  # Frecuencia de secuencia de video
        self.background_mean = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.background_mean = (
                (self.rho * self.background_mean) + ((1 - self.rho) * cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)))

    def detect(self, image):
        try:
            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            Mov = None
            MovT = None
            if image_gray.any():

                self.background_mean = ((self.rho * self.background_mean) + ((1 - self.rho) * image_gray))  # MF

                self.S = (self.rho * self.S) + ((1 - self.rho) * image_gray)

                probability_coefficient = np.sqrt(((image_gray - self.background_mean) ** 2) / self.S)

                Mov = probability_coefficient > 2
                MovT = np.uint8(Mov * image_gray)
            else:
                pass
            return Mov, MovT, self.background_mean
        except Exception as e:
            print("Error calculado moviminento" + str(e))
            return None, None, None

    @classmethod
    def getBackgroundMean(self):
        pass
