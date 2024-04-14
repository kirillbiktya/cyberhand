import argparse
import struct
from typing import List

import cyberhand.visualization as viz
from cyberhand import Manipulator, PAYLOAD_SIZE, PAYLOAD_STRUCT_FORMAT
from cyberhand.udp_client import UDPClient

parser = argparse.ArgumentParser(description='Клиент UDP-сервера, визуализирующий вращения сементов манипулятора')
parser.add_argument('--host', type=str, default='127.0.0.1', help='адрес сервера')
parser.add_argument('--port', type=int, default=8088, help='порт сервера')
parser.add_argument('--count', type=int, default=5, help='количество измерений')
parser.add_argument('--visualize', '-v', action='store_true',
                    help='если указано - будет показана визуализация измерений')

args = parser.parse_args()

manipulator_pos_list: List[Manipulator] = []  # список состояний манипулятора для кождого пакета измерений
client = UDPClient(args.host, args.port)
client.send_data(b"get")  # отправляем "запрос" get

for i in range(args.count):
    data = client.recv_data(PAYLOAD_SIZE)
    unpacked_data = struct.unpack(PAYLOAD_STRUCT_FORMAT, data)

    try:
        m = Manipulator(*unpacked_data)
        manipulator_pos_list.append(m)
        print(m)
    except Exception as e:
        # Manipulator.__init__ выбрасывает исключение только в том случае, если данных недостаточно
        # для заполнения списка сочленений
        print(e)
        break

client.finish()

if args.visualize:
    # ура! корявенькая визуализация!!!
    viz.get_pretty_plot(manipulator_pos_list)
