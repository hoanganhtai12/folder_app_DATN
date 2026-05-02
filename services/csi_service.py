# csi_service.py

# import threading
# from app.adapters.csi_eth_adapter import CsiEthAdapter  # Import adapter

# class CsiService:
#     def __init__(self, session_dir, session_t0):
#         # Cập nhật constructor để nhận session_t0
#         self.csi_adapter = CsiEthAdapter(session_dir, session_t0)  # Truyền session_t0 vào CsiEthAdapter

#     def start_csi_collection(self):
#         """Bắt đầu thu thập dữ liệu CSI."""
#         self.csi_thread = threading.Thread(target=self.csi_adapter.start_recording, daemon=True)
#         self.csi_thread.start()
#         print("CSI collection started.")

#     def stop_csi_collection(self):
#         """Dừng thu thập dữ liệu CSI."""
#         self.csi_adapter.stop()
#         self.csi_thread.join()
#         print("CSI collection stopped.")
# csi_service.py

import threading
from app.adapters.csi_eth_adapter import CsiEthAdapter


class CsiService:
    def __init__(self, session_dir, session_t0):
        self.csi_adapter = CsiEthAdapter(session_dir, session_t0)
        self.csi_thread = None

    def start_csi_collection(self):
        self.csi_thread = threading.Thread(
            target=self.csi_adapter.start_recording,
            daemon=True
        )
        self.csi_thread.start()
        print("CSI collection started.")

    def stop_csi_collection(self):
        self.csi_adapter.stop()

        if self.csi_thread and self.csi_thread.is_alive():
            self.csi_thread.join(timeout=5)

        print("CSI collection stopped.")