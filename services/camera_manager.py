import threading
import time

from app.adapters.webcam_adapter import WebcamAdapter


class CameraManager:
    def __init__(self):
        self.adapter = None
        self.thread = None
        self.lock = threading.Lock()

        self.running = False
        self.selected_camera_index = 0

        self.width = 640
        self.height = 480
        self.fps = 20

        self.latest_frame = None

    def list_cameras(self, max_index=5):
        available = []

        for index in range(max_index):
            cam = WebcamAdapter(camera_index=index)

            try:
                cam.open()
                ok, frame = cam.read_frame()

                if ok and frame is not None:
                    available.append(index)

            except Exception:
                pass

            finally:
                cam.close()

        return available

    def select_camera(self, cam_index: int):
        if self.running:
            self.stop()

        self.selected_camera_index = cam_index

        return {
            "status": "success",
            "cam_index": cam_index
        }

    def start(self, width=640, height=480, fps=20):
        if self.running:
            return {
                "status": "already_running",
                "cam_index": self.selected_camera_index
            }

        self.width = width
        self.height = height
        self.fps = fps

        self.adapter = WebcamAdapter(
            camera_index=self.selected_camera_index
        )

        self.adapter.open()

        self.running = True

        self.thread = threading.Thread(
            target=self._capture_loop,
            daemon=True
        )
        self.thread.start()

        return {
            "status": "started",
            "cam_index": self.selected_camera_index
        }

    def _capture_loop(self):
        frame_interval = 1.0 / self.fps

        while self.running:
            loop_start = time.perf_counter()

            ok, frame = self.adapter.read_frame()

            if ok and frame is not None:
                with self.lock:
                    self.latest_frame = frame.copy()

            elapsed = time.perf_counter() - loop_start
            time.sleep(max(0, frame_interval - elapsed))

    def stop(self):
        self.running = False

        if self.thread:
            self.thread.join(timeout=2)

        if self.adapter:
            self.adapter.close()

        self.thread = None
        self.adapter = None

        with self.lock:
            self.latest_frame = None

        return {
            "status": "stopped"
        }

    def get_frame(self):
        with self.lock:
            if self.latest_frame is None:
                return None

            return self.latest_frame.copy()

    def status(self):
        return {
            "running": self.running,
            "cam_index": self.selected_camera_index,
            "width": self.width,
            "height": self.height,
            "fps": self.fps,
            "has_frame": self.latest_frame is not None
        }


camera_manager = CameraManager()