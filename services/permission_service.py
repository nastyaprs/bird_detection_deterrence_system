from models.deterrence_permission import DeterrencePermission
from models.bird_detection import BirdDetection
from sqlalchemy.orm import joinedload
from models.recorded_video import RecordedVideo
from datetime import datetime
from sqlalchemy import func

class PermissionService:
    def __init__(self, session):
        self.session = session

    def create_permission(self, detection_id, user_id, allow: bool):
        permission = DeterrencePermission(
            detection_id=detection_id,
        )
        self.session.add(permission)
        self.session.commit()
        return permission
    
    def is_allowed(self, detection_id):
        self.session.expire_all()
        record = (
            self.session.query(DeterrencePermission)
            .filter_by(detection_id=detection_id)
            .first()
        )
        return record and record.allow

    def set_permission(self, detection_id, user_id, allow: bool):
        record = (
            self.session.query(DeterrencePermission)
            .filter_by(detection_id=detection_id)
            .first()
        )
        if not record:
            record = DeterrencePermission(
                detection_id=detection_id,
                user_id=user_id,
                allow=allow
            )
            self.session.add(record)
        else:
            record.allow = allow
            record.user_id = user_id
        self.session.commit()
    
    def is_denied(self, detection_id):
        self.session.expire_all()
        record = (
            self.session.query(DeterrencePermission)
            .filter_by(detection_id=detection_id)
            .first()
        )
        return record is not None and record.allow is False
    
    def get_pending_detections(self):
        subquery = (
            self.session.query(
                func.max(BirdDetection.id).label("latest_id"),
                RecordedVideo.camera_id
            )
            .join(DeterrencePermission, DeterrencePermission.detection_id == BirdDetection.id)
            .join(RecordedVideo, BirdDetection.video_id == RecordedVideo.id)
            .filter(DeterrencePermission.allow == None)
            .group_by(RecordedVideo.camera_id)
            .subquery()
        )

        return (
            self.session.query(BirdDetection)
            .options(joinedload(BirdDetection.video).joinedload(RecordedVideo.camera))
            .join(subquery, BirdDetection.id == subquery.c.latest_id)
            .all()
        )

    def allow(self, detection_id, user_id):
        existing = self.session.query(DeterrencePermission).filter_by(detection_id=detection_id).first()
        if existing:
            existing.allow = True
            existing.user_id = user_id
            existing.issued_at = datetime.now()
        else:
            permission = DeterrencePermission(
                detection_id=detection_id,
                user_id=user_id,
                allow=True
            )
            self.session.add(permission)
        self.session.commit()

    def deny(self, detection_id, user_id):
        existing = self.session.query(DeterrencePermission).filter_by(detection_id=detection_id).first()
        if existing:
            existing.allow = False
            existing.user_id = user_id
            existing.issued_at = datetime.now()
        else:
            permission = DeterrencePermission(
                detection_id=detection_id,
                user_id=user_id,
                allow=False
            )
            self.session.add(permission)
        self.session.commit()
