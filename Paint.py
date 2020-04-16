import matplotlib.pyplot as plt
import numpy as np


def paint_dot(task, m, x_max, y_max):
    fig = plt.figure(figsize=(5, 5))
    ax = fig.gca()
    ax.set_xticks(np.arange(0, x_max + 1, 5))
    ax.set_yticks(np.arange(0, y_max + 1, 5))

    # y 轴不可见
    ax.axes.get_yaxis().set_visible(False)
    # x 轴不可见
    ax.axes.get_xaxis().set_visible(False)
    # 去掉边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    x = map(lambda point: point.x, task.points)
    y = map(lambda point: point.y, task.points)

    plt.scatter(list(x), list(y), alpha=0.5)

    x1 = map(lambda user: user.position[0], m)
    y1 = map(lambda user: user.position[1], m)
    plt.scatter(list(x1), list(y1))
    # plt.grid(True)
    plt.rc('grid', linestyle="-", color='black')

    plt.show()


if __name__ == '__main__':
    N = 10
    s = (30 * np.random.rand(N)) ** 2
    # 随机颜色
    c = np.random.rand(N)

    print(s, c)
