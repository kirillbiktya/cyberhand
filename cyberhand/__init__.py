import struct
from dataclasses import dataclass
from typing import List

import numpy as np

# Параметры манипулятора, заданные в ТЗ
MANIPULATOR_JOINTS_COUNT = 6
PAYLOAD_STRUCT_FORMAT = "I{}d".format(MANIPULATOR_JOINTS_COUNT)
PAYLOAD_SIZE = struct.calcsize(PAYLOAD_STRUCT_FORMAT)
JOINT_CONFIGURATION = [
    {"number": 0, "a": 0., "d": 0.21, "alpha": np.pi / 2},
    {"number": 1, "a": -0.8, "d": 0.193, "alpha": 0},
    {"number": 2, "a": -0.598, "d": -0.16, "alpha": 0},
    {"number": 3, "a": 0., "d": 0.25, "alpha": np.pi / 2},
    {"number": 4, "a": 0., "d": 0.25, "alpha": -np.pi / 2},
    {"number": 5, "a": 0., "d": 0.25, "alpha": 0}
]


def cosd(deg: float) -> float: return np.cos(np.deg2rad(deg))


def sind(deg: float) -> float: return np.sin(np.deg2rad(deg))


@dataclass
class Joint:
    number: int
    a: float
    d: float
    alpha: float
    theta: float

    def transform_matrix(self):
        """
        Возвращает матрицу преобразований конкретно для данного сочленения

        :return:
        """
        return np.array([
            [cosd(self.theta), -sind(self.theta) * cosd(self.alpha), sind(self.theta) * sind(self.alpha),
             self.a * cosd(self.theta)],
            [sind(self.theta), cosd(self.theta) * cosd(self.alpha), -cosd(self.theta) * sind(self.alpha),
             self.a * sind(self.theta)],
            [0, sind(self.alpha), cosd(self.alpha), self.d],
            [0, 0, 0, 1]
        ])


class Manipulator:
    def __init__(self, timestamp: int, *theta_list: List[float]):
        self.timestamp = timestamp

        if len(theta_list) != MANIPULATOR_JOINTS_COUNT:
            raise Exception("invalid data batch")

        self.joints: List[Joint] = []

        # матрица преобразований от n=0 до n=6
        self.head_position_matrix = np.zeros((4, 4))

        for i, theta in enumerate(theta_list):
            joint = Joint(**JOINT_CONFIGURATION[i], theta=theta)
            self.joints.append(joint)
            if i == 0:
                self.head_position_matrix = joint.transform_matrix()
            else:
                self.head_position_matrix = np.matmul(self.head_position_matrix, joint.transform_matrix())

        # декартовы координаты запястья
        self.head_position_decart = self.head_position_matrix[[0, 1, 2], :][:, 3]
        # TODO: углы Эйлера запястья

    def __repr__(self):
        return ("timestamp: {} x: {} y: {} z: {}"
                .format(self.timestamp, *self.head_position_decart))

    def __str__(self):
        return self.__repr__()

    def get_all_joint_positions_for_pretty_plot(self):
        """
        Возвращает значения, необходимые для cyberhand.vuzualization.get_pretty_plot()
        Отметка: возвращает отдельные списки координат начала и конца каждого сегмента.

        :return:
        """
        xs = [0, ]
        ys = [0, ]
        zs = [0, ]
        current_transform_matrix = np.zeros((4, 4))
        for joint in self.joints:
            if joint.number == 0:
                current_transform_matrix = joint.transform_matrix()
            else:
                current_transform_matrix = np.matmul(current_transform_matrix, joint.transform_matrix())

            xs.append(current_transform_matrix[0, 3])
            ys.append(current_transform_matrix[1, 3])
            zs.append(current_transform_matrix[2, 3])

        return xs, ys, zs
