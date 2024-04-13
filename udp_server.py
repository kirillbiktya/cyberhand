# Полностью повторяет функционал main.c, создан только потому что не было доступа
# к Unix/Linux в момент работы над кодом

import socketserver
import struct

thetas = [
    [10.0, -50.0, -60.0, 90.0, 50.0, 0.0],
    [0.0, -90.0, 0.0, -90.0, 0.0, 0.0],
    [60.0, 60.0, 60.0, 60.0, 60.0, 60.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [179.0, 223.0, -74.0, 35.0, 65.0, 0.0]
]


class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        data = self.request[0]
        socket = self.request[1]
        if len(data) == 3:
            for i, theta in enumerate(thetas):
                socket.sendto(struct.pack("I6d", i, *theta), self.client_address)


server = socketserver.UDPServer(("127.0.0.1", 8088), RequestHandler)
server.serve_forever()
