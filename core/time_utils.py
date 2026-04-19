from datetime import datetime, timezone
import time
import uuid

def utc_now():
    return datetime.now(timezone.utc)

def utc_now_iso():
    return utc_now().isoformat()

def perf_now():
    return time.perf_counter()

def new_session_id():
    return uuid.uuid4().hex