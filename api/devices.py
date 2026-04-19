# API trạng thái thiết bị (CSI, webcam)
from fastapi import APIRouter

router = APIRouter(prefix="/api/devices", tags=["devices"])

@router.post("/test-audio")
def test_audio():
    return {"status": "audio_test_triggered"}