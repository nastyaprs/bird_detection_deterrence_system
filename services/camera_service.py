from sqlalchemy.orm import Session
from models.camera import Camera

class CameraService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Camera).all()

    def get_by_id(self, camera_id: int):
        return self.db.query(Camera).filter(Camera.id == camera_id).first()

    def create(self, name: str, location: str, interface_type: str, device_path: str, model: str):
        camera = Camera(
            name=name,
            interface_type=interface_type,
            device_path=device_path,
            model=model
        )
        self.db.add(camera)
        self.db.commit()
        self.db.refresh(camera)
        return camera

    def update(self, camera_id: int, **kwargs):
        camera = self.get_by_id(camera_id)
        if not camera:
            return None
        for key, value in kwargs.items():
            if hasattr(camera, key):
                setattr(camera, key, value)
        self.db.commit()
        return camera

    def delete(self, camera_id: int):
        camera = self.get_by_id(camera_id)
        if camera:
            self.db.delete(camera)
            self.db.commit()
            return True
        return False
