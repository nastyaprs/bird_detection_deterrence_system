from sqlalchemy.orm import Session
from models.bird_detection import BirdDetection

class BirdDetectionService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(BirdDetection).all()

    def get_by_id(self, detection_id: int):
        return self.db.query(BirdDetection).filter(BirdDetection.id == detection_id).first()

    def create(self, timestamp, video_id, confidence, bird_lowest_amount, bird_highest_amount, videopath):
        detection = BirdDetection(
            timestamp=timestamp,
            video_id=video_id,
            confidence=confidence,
            bird_lowest_amount=bird_lowest_amount,
            bird_highest_amount=bird_highest_amount,
            video_path=videopath
        )
        self.db.add(detection)
        self.db.commit()
        self.db.refresh(detection)
        return detection

    def update(self, detection_id: int, **kwargs):
        detection = self.get_by_id(detection_id)
        if not detection:
            return None
        for key, value in kwargs.items():
            if hasattr(detection, key):
                setattr(detection, key, value)
        self.db.commit()
        return detection

    def delete(self, detection_id: int):
        detection = self.get_by_id(detection_id)
        if detection:
            self.db.delete(detection)
            self.db.commit()
            return True
        return False
