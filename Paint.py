import matplotlib.pyplot as plt
import numpy as np


def paint_dot(task, m, x_max, y_max):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.gca()
    ax.set_xticks(np.arange(0, x_max + 1, 5))
    ax.set_yticks(np.arange(0, y_max + 1, 5))

    x = map(lambda point: point.x, task.points)
    y = map(lambda point: point.y, task.points)
    plt.scatter(list(x), list(y))

    x1 = map(lambda user: user.position[0], m)
    y1 = map(lambda user: user.position[1], m)
    plt.scatter(list(x1), list(y1))
    plt.grid(True)
    plt.rc('grid', linestyle="-", color='black')

    plt.show()
