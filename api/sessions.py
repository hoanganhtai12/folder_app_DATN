# API quản lý session

from fastapi import APIRouter

router = APIRouter(prefix="/api/sessions", tags=["sessions"])

@router.post("/start")
def start_session():
    return {"status": "started"}

@router.post("/stop")
def stop_session():
    return {"status": "stopped"}