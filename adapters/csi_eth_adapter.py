# # csi_eth_adapter.py

# import csv
# import random
# import time
# from app.core.time_utils import utc_now_iso, perf_now

# class CsiEthAdapter:
#     def __init__(self, session_dir):
#         self.session_dir = session_dir
#         self.raw_eth_file = open(f"{session_dir}/raw_eth.csv", "w", newline='')
#         self.writer = csv.writer(self.raw_eth_file)
#         self.writer.writerow(["elapsed_sec", "packet_id", "data", "timestamp_utc"])  # Header for raw_eth.csv
        
#         self.start_time = perf_now()  # Lưu thời gian bắt đầu khi bắt đầu thu thập dữ liệu
#         self.recording = True  # Biến để kiểm soát trạng thái thu thập dữ liệu

#     def generate_fake_csi_data(self):
#         """Giả lập dữ liệu CSI ngẫu nhiên."""
#         data = random.getrandbits(8 * 10).to_bytes(10, byteorder='big')
#         # Tính toán elapsed_sec từ start_time để đồng bộ thời gian
#         elapsed_sec = perf_now() - self.start_time
#         packet_id = random.randint(1, 1000)
#         return elapsed_sec, packet_id, data

#     def start_recording(self):
#         """Bắt đầu thu thập dữ liệu CSI giả và ghi vào file."""
#         try:
#             while self.recording:  # Kiểm soát quá trình thu thập dữ liệu
#                 elapsed_sec, packet_id, data = self.generate_fake_csi_data()
#                 timestamp_utc = utc_now_iso()  # Ghi timestamp UTC của mỗi gói dữ liệu
#                 self.writer.writerow([elapsed_sec, packet_id, data.hex(), timestamp_utc])
#                 time.sleep(0.01)  # Giả lập thời gian giữa các gói dữ liệu
#         except Exception as e:
#             print(f"Error during CSI recording: {e}")

#     def stop(self):
#         """Dừng ghi dữ liệu vào file raw_eth.csv."""
#         self.recording = False  # Dừng quá trình thu thập dữ liệu
#         self.raw_eth_file.close()  # Đảm bảo đóng file sau khi thu thập dữ liệu xong


# csi_eth_adapter.py

import csv
import random
import time
from app.core.time_utils import utc_now_iso, perf_now

class CsiEthAdapter:
    def __init__(self, session_dir, session_t0):
        self.session_dir = session_dir
        self.session_t0 = session_t0  # Nhận thời gian bắt đầu từ bên ngoài (ví dụ từ main)
        self.raw_eth_file = open(f"{session_dir}/raw_eth.csv", "w", newline='')
        self.writer = csv.writer(self.raw_eth_file)
        self.writer.writerow(["elapsed_sec", "packet_id", "data", "timestamp_utc"])  # Header for raw_eth.csv
        
        self.start_time = perf_now()  # Lưu thời gian bắt đầu khi bắt đầu thu thập dữ liệu

    def generate_fake_csi_data(self):
        """Giả lập dữ liệu CSI ngẫu nhiên."""
        data = random.getrandbits(8 * 10).to_bytes(10, byteorder='big')
        # Tính toán elapsed_sec từ session_t0 để đồng bộ thời gian
        elapsed_sec = perf_now() - self.start_time  # Thời gian trôi qua kể từ khi bắt đầu thu thập
        packet_id = random.randint(1, 1000)
        return elapsed_sec, packet_id, data

    def start_recording(self):
        """Bắt đầu thu thập dữ liệu CSI giả và ghi vào file."""
        try:
            while True:
                elapsed_sec, packet_id, data = self.generate_fake_csi_data()
                timestamp_utc = utc_now_iso()  # Ghi timestamp UTC của mỗi gói dữ liệu
                self.writer.writerow([elapsed_sec, packet_id, data.hex(), timestamp_utc])
                time.sleep(0.01)  # Giả lập thời gian giữa các gói dữ liệu
        except Exception as e:
            print(f"Error during CSI recording: {e}")

    def stop(self):
        """Dừng ghi dữ liệu vào file raw_eth.csv."""
        self.raw_eth_file.close()  # Đảm bảo đóng file sau khi thu thập dữ liệu xong