from sqlalchemy.orm import Session
from models.recorded_video import RecordedVideo

class RecordedVideoService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(RecordedVideo).all()

    def get_by_id(self, video_id: int):
        return self.db.query(RecordedVideo).filter(RecordedVideo.id == video_id).first()

    def create(self, start_time, end_time, file_path, camera_id=None, note=None):
        video = RecordedVideo(
            start_time=start_time,
            end_time=end_time,
            file_path=file_path,
            camera_id=camera_id,
            note=note
        )
        self.db.add(video)
        self.db.commit()
        self.db.refresh(video)
        return video

    def update(self, video_id: int, **kwargs):
        video = self.get_by_id(video_id)
        if not video:
            return None
        for key, value in kwargs.items():
            if hasattr(video, key):
                setattr(video, key, value)
        self.db.commit()
        return video

    def delete(self, video_id: int):
        video = self.get_by_id(video_id)
        if video:
            self.db.delete(video)
            self.db.commit()
            return True
        return False
