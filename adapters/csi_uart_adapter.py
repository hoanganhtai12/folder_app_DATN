import serial
import time
import random

# Mở cổng UART (ví dụ '/dev/ttyUSB0' trên Linux hoặc 'COM3' trên Windows)
#ser = serial.Serial('COM3', 9600)

def generate_fake_data():
    # Giả lập dữ liệu CSI (mỗi gói dữ liệu là 10 byte ngẫu nhiên)
    data = random.getrandbits(8 * 10).to_bytes(10, byteorder='big')
    return data

while True:
    # Gửi dữ liệu giả mỗi 1 giây
    fake_data = generate_fake_data()
   # ser.write(fake_data)
    print(f"Sent: {fake_data.hex()}")
    time.sleep(1)  # Giả lập tốc độ truyền dữ liệu