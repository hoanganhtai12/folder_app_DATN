from app.core.config import SESSIONS_DIR
from app.core.time_utils import new_session_id, utc_now_iso

class SessionService:
    def create_session(self):
        session_id = new_session_id()
        session_dir = SESSIONS_DIR / session_id

        (session_dir / "csi").mkdir(parents=True, exist_ok=True)
        (session_dir / "video").mkdir(parents=True, exist_ok=True)
        (session_dir / "labels").mkdir(parents=True, exist_ok=True)
        (session_dir / "logs").mkdir(parents=True, exist_ok=True)
        (session_dir / "sync").mkdir(parents=True, exist_ok=True)

        session_info = {
            "session_id": session_id,
            "start_time_utc": utc_now_iso(),
            "status": "running"
        }

        return session_info, session_dir