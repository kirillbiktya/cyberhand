import struct
from typing import List

import cyberhand.visualization as viz
from cyberhand import Manipulator, PAYLOAD_SIZE, PAYLOAD_STRUCT_FORMAT
from cyberhand.udp_client import UDPClient

visualize = False  # ура! корявенькая визуализация!!!

server_addr = ("127.0.0.1", 8088)
payloads_count = 5

manipulator_pos_list: List[Manipulator] = []  # список состояний манипулятора для кождого пакета измерений
client = UDPClient(*server_addr)
client.send_data(b"ABC")

for i in range(payloads_count):
    data = client.recv_data(PAYLOAD_SIZE)
    unpacked_data = struct.unpack(PAYLOAD_STRUCT_FORMAT, data)

    print(unpacked_data)

    try:
        m = Manipulator(*unpacked_data)
        manipulator_pos_list.append(m)
        print(m)
    except Exception as e:
        print(str(e))
        print("Наверняка мы бы здесь поняли, что raise в __init__ ни к чему хорошему привести не может")

client.finish()

if visualize:
    viz.get_pretty_plot(manipulator_pos_list)
