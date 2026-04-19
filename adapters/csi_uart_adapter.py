import socket

class CsiEthAdapter:
    def __init__(self, host="0.0.0.0", port=9000, buffer_size=4096):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.sock = None

    def open(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

    def read_packet(self):
        data, addr = self.sock.recvfrom(self.buffer_size)
        return data, addr

    def close(self):
        if self.sock:
            self.sock.close()