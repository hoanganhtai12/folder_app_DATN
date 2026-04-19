# API kiểm tra tình trạng hệ thống

from fastapi import APIRouter

router = APIRouter(prefix="/api/health", tags=["health"])

@router.get("")
def get_health():
    return {"status": "ok"}