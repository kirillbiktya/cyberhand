import socket


class UDPClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_data(self, buffer):
        self.socket.sendto(buffer, (self.host, self.port))

    def recv_data(self, bufsize):
        data, addr = self.socket.recvfrom(bufsize)
        return data

    def finish(self):
        self.socket.close()
