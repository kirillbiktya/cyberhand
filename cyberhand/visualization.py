# Не уверен, что верно понял, как работает 3d matplotlib, но что-то вроде получилось

from typing import List

import matplotlib.pyplot as plt
from matplotlib import animation

from cyberhand import Manipulator

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
lines = []


def initial_plot():
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(-1.5, 1.5)
    for i in range(0, 5):
        line_obj, = ax.plot(xs=[], ys=[], zs=[])
        lines.append(line_obj)
    return lines


def animate(m):
    frame = m.get_all_joint_positions_for_pretty_plot()
    for i in range(0, 5):
        lines[i].set_data_3d(frame[0][i:i + 2], frame[1][i:i + 2], frame[2][i:i + 2])
    return lines


def get_pretty_plot(m_list: List[Manipulator]):
    anim = animation.FuncAnimation(fig, animate, frames=m_list, init_func=initial_plot, interval=500)
    # anim.save("data.gif")
    plt.show()
