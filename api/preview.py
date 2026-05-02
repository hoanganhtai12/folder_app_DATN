import cv2
import time

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()


def generate_frames():
    cap = cv2.VideoCapture(0)

    try:
        while True:
            ok, frame = cap.read()

            if not ok:
                time.sleep(0.1)
                continue

            ret, buffer = cv2.imencode(".jpg", frame)

            if not ret:
                continue

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" +
                buffer.tobytes() +
                b"\r\n"
            )

    finally:
        cap.release()


@router.get("/video")
def video_preview():
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )