import socket


class UDPClient:
    def __init__(self, host: str, port: int):
        """
        Простой клиент для UDP

        :param host: адрес сервера
        :param port: порт сервера
        """
        self.host = host
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_data(self, buffer: bytes) -> None:
        self.socket.sendto(buffer, (self.host, self.port))

    def recv_data(self, bufsize: int) -> bytes:
        data, addr = self.socket.recvfrom(bufsize)
        return data

    def finish(self):
        self.socket.close()
