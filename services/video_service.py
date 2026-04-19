import cv2
from pathlib import Path
from app.core.time_utils import utc_now_iso

class VideoService:
    def __init__(self, session_dir: Path, fps=20.0, width=640, height=480):
        self.session_dir = session_dir
        self.fps = fps
        self.width = width
        self.height = height
        self.video_path = session_dir / "video" / "cam1.mp4"
        self.index_path = session_dir / "video" / "video_index.csv"
        self.writer = None
        self.frame_no = 0

        if not self.index_path.exists():
            self.index_path.write_text("frame_no,timestamp_utc\n", encoding="utf-8")

    def open(self):
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.writer = cv2.VideoWriter(
            str(self.video_path),
            fourcc,
            self.fps,
            (self.width, self.height)
        )

    def write_frame(self, frame):
        self.frame_no += 1
        self.writer.write(frame)
        with open(self.index_path, "a", encoding="utf-8") as f:
            f.write(f"{self.frame_no},{utc_now_iso()}\n")

    def close(self):
        if self.writer:
            self.writer.release()