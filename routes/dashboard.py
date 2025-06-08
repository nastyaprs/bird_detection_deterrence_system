from flask import render_template, redirect, url_for, request, session
from services.bird_detection_service import BirdDetectionService
from services.recorded_video_service import RecordedVideoService
from services.mode_service import ModeService
from services.deterrence_service import DeterrenceService
from config import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .decorators import login_required
from models.enums.system_mode import SystemMode
from services.permission_service import PermissionService

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
db_session = Session()

bird_service = BirdDetectionService(db_session)
video_service = RecordedVideoService(db_session)
mode_service = ModeService(db_session)

def index():
    mode = mode_service.get_mode()
    return render_template("home.html", mode=mode, SystemMode=SystemMode)

@login_required
def detections():
    all_detections = bird_service.get_all()
    return render_template("detections.html", detections=all_detections)

@login_required
def videos():
    all_videos = video_service.get_all()
    return render_template("videos.html", videos=all_videos)

@login_required
def deterrence():
    deterrence_service = DeterrenceService(db_session)
    actions = deterrence_service.get_all_actions()
    return render_template("deterrence.html", actions=actions)

@login_required
def toggle_mode():
    if request.method == "POST":
        selected = request.form.get("mode")
        mode_service.set_mode(SystemMode[selected].value)
        return redirect(url_for("index"))
    current = mode_service.get_mode()
    return render_template("toggle_mode.html", current_mode=current, SystemMode=SystemMode)

@login_required
def start_deterrence():
    camera_id = int(request.form.get("camera_id"))
    detection_id = int(request.form.get("detection_id"))
    user_id = session.get("user_id")

    deterrence_service = DeterrenceService(db_session)
    deterrence_service.activate(camera_id=camera_id, detection_id=detection_id, user_id=user_id)

    return redirect(url_for("control_view", camera_id=camera_id))

@login_required
def control_view():
    permission_service = PermissionService(db_session)
    pending_detections = permission_service.get_pending_detections()
    return render_template("control.html", detections=pending_detections)

@login_required
def grant_permission():
    detection_id = int(request.form.get("detection_id"))
    user_id = session.get("user_id")
    permission_service = PermissionService(db_session)
    permission_service.allow(detection_id, user_id)
    return redirect(url_for("control_view"))

@login_required
def deny_permission():
    detection_id = int(request.form.get("detection_id"))
    user_id = session.get("user_id")
    permission_service = PermissionService(db_session)
    permission_service.deny(detection_id, user_id)
    return redirect(url_for("control_view"))
