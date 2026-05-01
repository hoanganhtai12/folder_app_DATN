

# import threading
# import time
# from app.services.csi_service import start_csi_data_collection  # Import từ csi_service
# from app.services.video_service import start_video_recording  # Import từ video_service
# from app.services.audio_cue_service import play_audio  # Import từ audio_cue_service

# # Hàm đồng bộ hóa video, audio và dữ liệu CSI
# def synchronize_data_collection(session_dir, stop_event):
#     # Bắt đầu thu thập dữ liệu CSI
#     stop_csi_event = threading.Event()
#     csi_thread = start_csi_data_collection(session_dir, stop_csi_event)
    
#     # Bắt đầu quay video
#     video_thread = threading.Thread(target=start_video_recording, args=(session_dir, stop_event), daemon=True)
#     video_thread.start()

#     # Phát audio cue
#     audio_thread = threading.Thread(target=play_audio, args=(session_dir,), daemon=True)
#     audio_thread.start()

#     # Đợi video và audio phát hoàn tất
#     video_thread.join()
#     audio_thread.join()

#     # Dừng thu thập CSI khi video và audio kết thúc
#     stop_csi_event.set()
#     print("Data collection completed: Video, Audio, and CSI.")

# sync_service.py

import threading
import time

class SyncService:
    def __init__(self, video_ready_event, csi_adapter):
        self.video_ready_event = video_ready_event
        self.csi_adapter = csi_adapter

    def sync_audio_video_csi(self):
        """Đồng bộ audio, video và CSI."""
        print("Chờ video sẵn sàng...")
        if not self.video_ready_event.wait(timeout=10):
            raise RuntimeError("Camera chưa ghi được frame đầu tiên sau 10 giây")

        print("Video đã sẵn sàng. Bắt đầu đồng bộ với CSI.")

        # Thực hiện đồng bộ video + audio + CSI ở đây
        # Có thể bổ sung logic xử lý đồng bộ trong khi chạy video và thu thập dữ liệu CSI

        time.sleep(0.5)  # Cho video ghi thêm một đoạn ngắn trước khi phát audio

        # Gọi hàm thu thập audio, video và ghi dữ liệu CSI tại đây
        self.csi_adapter.start_recording()