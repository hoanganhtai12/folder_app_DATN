import random
import time

# Hàm giả lập nhận dữ liệu CSI ngẫu nhiên
def generate_fake_csi_data():
    # Tạo dữ liệu ngẫu nhiên giả
    data = random.getrandbits(8 * 10).to_bytes(10, byteorder='big')
    elapsed_sec = time.time()  # Lấy thời gian thực tế làm elapsed_sec
    packet_id = random.randint(1, 1000)
    
    return elapsed_sec, packet_id, data

# Hàm giả lập nhận và xử lý dữ liệu CSI
def process_fake_csi_data():
    #for _ in range(5):  # Giả lập nhận 5 gói dữ liệu
    while True:
        elapsed_sec, packet_id, data = generate_fake_csi_data()
        
        # Xử lý gói dữ liệu (in ra cho demo)
        print(f"Processing packet {packet_id} with data {data.hex()} at {elapsed_sec} sec")
        
        # Giả lập việc đồng bộ dữ liệu (chờ 1 giây giữa mỗi gói dữ liệu)
        time.sleep(0.01)

# Chạy thử
if __name__ == "__main__":
    process_fake_csi_data()