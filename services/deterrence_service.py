from models.platform import Platform
from models.deterrence_action import DeterrenceAction
from sqlalchemy.orm import Session
from datetime import datetime

class DeterrenceService:
    def __init__(self, session: Session):
        self.session = session

    def activate(self, camera_id: int, detection_id: int, user_id: int = None):
        platform = (
            self.session.query(Platform)
            .filter(Platform.camera_id == camera_id)
            .first()
        )

        if not platform or not platform.deterrent_system:
            print(f"⚠️ Не знайдено платформу або систему відлякування для камери ID {camera_id}")
            return

        deterrent = platform.deterrent_system

        print(f"🔊 Відлякування активовано для камери ID {camera_id} з використанням {deterrent.model}")

        action = DeterrenceAction(
            timestamp=datetime.now(),
            detection_id=detection_id,
            deterrent_id=deterrent.id,
            user_id=user_id
        )
        self.session.add(action)
        self.session.commit()

    def get_all_actions(self):
        return self.session.query(DeterrenceAction).order_by(DeterrenceAction.timestamp.desc()).all()
