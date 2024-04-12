from typing import List, Tuple
import struct
from .udp_client import UDPClient
import numpy as np
from dataclasses import dataclass


PAYLOAD_COUNT = 5

MANIPULATOR_JOINTS_COUNT = 6

PAYLOAD_STRUCT_FORMAT = "I6d"
PAYLOAD_SIZE = struct.calcsize(PAYLOAD_STRUCT_FORMAT)


JOINT_CONFIGURATION = [
    {"number": 0,   "a": 0.,     "d": 0.21,  "alpha": np.pi / 2},
    {"number": 1,   "a": -0.8,   "d": 0.193, "alpha": 0},
    {"number": 2,   "a": -0.598, "d": -0.16, "alpha": 0},
    {"number": 3,   "a": 0.,     "d": 0.25,  "alpha": np.pi / 2},
    {"number": 4,   "a": 0.,     "d": 0.25,  "alpha": -np.pi / 2},
    {"number": 5,   "a": 0.,     "d": 0.25,  "alpha": 0}
]


@dataclass
class Joint:
    number: int
    a: float
    d: float
    alpha: float
    theta: float

    decart: Tuple[float, float, float] = (0, 0, 0)

    def get_dh_matrix(self):
        return np.array([
            [np.cos(self.theta), -np.sin(self.theta)*np.cos(self.alpha), np.sin(self.theta)*np.sin(self.alpha), self.a*np.cos(self.theta)],
            [np.sin(self.theta), np.cos(self.theta)*np.cos(self.alpha), -np.cos(self.theta)*np.sin(self.alpha), self.a*np.sin(self.theta)],
            [0, np.sin(self.alpha), np.cos(self.alpha), self.d],
            [0, 0, 0, 1]
        ])


@dataclass
class ManipulatorPos:
    def __init__(self, timestamp: int, *theta_list):
        self.timestamp = timestamp

        if len(theta_list) != MANIPULATOR_JOINTS_COUNT:
            raise Exception("invalid data batch")

        self.joints: List[Joint] = []

        for i, theta in enumerate(theta_list):
            self.joints.append(
                Joint(**JOINT_CONFIGURATION[i], theta=theta)
            )


class PosEstimator:
    def __init__(self, data_source_addr=("127.0.0.1", 8088)):
        self.data_source_addr = data_source_addr

        self.manipulator_pos_list: List[ManipulatorPos] = []

    def _receive_data_batch(self):
        client = UDPClient(*self.data_source_addr)

        client.send_data(b"ABC")

        for i in range(PAYLOAD_COUNT):
            data = client.recv_data(PAYLOAD_SIZE)
            unpacked_data = struct.unpack(PAYLOAD_STRUCT_FORMAT, data)

            print(unpacked_data)

            m = ManipulatorPos(*unpacked_data)
            self.manipulator_pos_list.append(m)

        client.finish()



