import cv2
import numpy as np


class VideoProcessor:
    def denoise(self, frame):
        return cv2.fastNlMeansDenoisingColored(frame, None, 5, 5, 7, 21)

    def correct_lighting(self, frame):
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l_clahe = clahe.apply(l)
        lab = cv2.merge((l_clahe, a, b))
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    def normalize_contrast(self, frame):
        gamma = 1.2
        lookup_table = np.array([((i / 255.0) ** (1 / gamma)) * 255
                                 for i in range(256)]).astype("uint8")
        return cv2.LUT(frame, lookup_table)

    def process(self, frame):
        frame = self.denoise(frame)
        frame = self.correct_lighting(frame)
        frame = self.normalize_contrast(frame)
        return frame
