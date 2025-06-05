from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .user import User
from .recorded_video import RecordedVideo
from .bird_detection import BirdDetection
from .deterrence_action import DeterrenceAction
from .camera import Camera
from .deterrent_system import DeterrentSystem