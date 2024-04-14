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
    """
    Класс, описывающий сочленение.
    """
    number: int
    a: float
    d: float
    alpha: float
    theta: float

    def transform_matrix(self) -> np.ndarray[(4, 4), np.dtype[float]]:
        """
        Возвращает матрицу преобразований конкретно для данного сочленения, без учета преобразований предыдущих
        сочленений

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
    """
    Класс, описывающий состояние манипулятора в конкретный момент времени
    """

    def __init__(self, timestamp: int, *theta_list: List[float]):
        """

        :param timestamp: Номер измерения
        :param theta_list: Список углов theta для всех сочленений манипулятора
        """
        self.timestamp = timestamp

        if len(theta_list) != MANIPULATOR_JOINTS_COUNT:
            if len(theta_list) < MANIPULATOR_JOINTS_COUNT:
                raise Exception("invalid data batch")
            else:
                theta_list = theta_list[:MANIPULATOR_JOINTS_COUNT]

        self.joints: List[Joint] = []

        for i, theta in enumerate(theta_list):
            joint = Joint(**JOINT_CONFIGURATION[i], theta=theta)
            self.joints.append(joint)

    def __repr__(self):
        return ("timestamp: {} \tx: {:3.4f} \ty: {:3.4f} \tz: {:3.4f} \tax: {:3.4f} \tay {:3.4f} \taz {:3.4f}"
                .format(self.timestamp, *self.head_decart(), *self.head_euler()))

    def __str__(self):
        return self.__repr__()

    def get_transform_matrix_by_joint_number(self, joint_number):
        """
        Матрица трансформаций относительно начала координат для сочленения №joint_number,
        с учетом предыдущих трансформаций

        :param joint_number: номер сочленения
        :return:
        """
        self.joints.sort(key=lambda joint: joint.number)
        transform_matrix = None
        for joint in self.joints:
            if transform_matrix is None:
                transform_matrix = joint.transform_matrix()
            transform_matrix = np.matmul(transform_matrix, joint.transform_matrix())
            if joint.number == joint_number:
                break

        return transform_matrix

    def get_decart_by_joint_number(self, joint_number):
        """
        Декартовы координаты сочленения №joint_number относительно начала координат

        :param joint_number: номер сочленения
        :return:
        """
        return self.get_transform_matrix_by_joint_number(joint_number)[[0, 1, 2], :][:, 3]

    def get_euler_by_joint_number(self, joint_number):
        """
        Эйлеровы углы поворота сочленения №joint_number относительно начала координат

        :param joint_number: номер сочленения
        :return:
        """
        m = self.get_transform_matrix_by_joint_number(joint_number)
        if m[0, 2] < 1.:
            if m[0, 2] > -1.:
                ay = np.arcsin(m[0, 2])
                ax = np.arctan2(-m[1, 2], m[2, 2])
                az = np.arctan2(-m[0, 1], m[0, 0])
            else:  # m[0, 2] == -1.
                ay = -np.pi / 2
                ax = -np.arctan2(m[1, 0], m[1, 1])
                az = 0.
        else:  # m[0, 2] == 1.
            ay = np.pi / 2
            ax = np.arctan2(m[1, 0], m[1, 1])
            az = 0.

        return np.rad2deg(ax), np.rad2deg(ay), np.rad2deg(az)

    def head_decart(self):
        """
        Декартовы координаты кисти манипулятора относительно начала координат

        :return:
        """
        return self.get_transform_matrix_by_joint_number(len(self.joints) - 1)[[0, 1, 2], :][:, 3]

    def head_euler(self):
        """
        Эйлеровы углы поворота кисти относительно начала координат

        :return:
        """
        return self.get_euler_by_joint_number(len(self.joints) - 1)

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
