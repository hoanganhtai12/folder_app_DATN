# API quản lý session

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Literal

from app.services.recording_service import RecordingService

router = APIRouter()

recorder = RecordingService()


class CameraConfig(BaseModel):
    enabled: bool = True
    camera_index: int = 0
    fps: int = 20
    width: int = 640
    height: int = 480


class UartConfig(BaseModel):
    enabled: bool = True
    port: str = "COM3"
    baudrate: int = 115200


class EthernetConfig(BaseModel):
    enabled: bool = True
    host: str = "0.0.0.0"
    port: int = 9000
    protocol: Literal["udp", "tcp"] = "udp"


class DevicesConfig(BaseModel):
    camera: CameraConfig
    uart: UartConfig
    ethernet: EthernetConfig


class StartSessionRequest(BaseModel):
    scenario: str
    repeat_count: int
    position_id: int
    devices: DevicesConfig


@router.post("/start")
def start_session(config: StartSessionRequest):
    return recorder.start(config.model_dump())


@router.post("/stop")
def stop_session():
    return recorder.stop()