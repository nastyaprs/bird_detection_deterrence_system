import numpy as np
from ultralytics import YOLO


class BirdDetector:
    def __init__(self, model_path: str, conf: float = 0.25, device: str = 'cpu'):
        self.model = YOLO(model_path)
        self.conf = conf
        self.device = device

    def detect(self, frame: np.ndarray):
        results = self.model.predict(
            source=frame,
            save=False,
            conf=self.conf,
            device=self.device,
            verbose=False
        )
        return results[0]