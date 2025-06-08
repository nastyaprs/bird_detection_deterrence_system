from models.system_state import SystemState
from models.enums.system_mode import SystemMode
from datetime import datetime

class ModeService:
    def __init__(self, session):
        self.session = session

    def get_mode(self):
        state = (
            self.session.query(SystemState)
            .order_by(SystemState.date_in.desc())
            .first()
        )
        if state:
            return state.mode
        return SystemMode.auto.name

    def set_mode(self, mode):
        new_state = SystemState(
            mode=mode,
            date_in=datetime.now()
        )
        self.session.add(new_state)
        self.session.commit()
