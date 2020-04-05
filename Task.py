import random
import matplotlib.pyplot as plt
import numpy as np


# 任务类
class Task:
    # 初始化一个任务
    def __init__(self, time, budget, points):
        # 任务时间
        self.time = time
        # 预算
        self.budget = budget
        # 兴趣点集合
        self.points = points
        # 实际完成的数据点情况
        self.actual_points = [0 for _ in range(len(points))]
        # 总数据量
        self.data = calculate_data(points)


# 兴趣点类
class Point:
    # 初始化一个兴趣点
    def __init__(self, _id, x, y, data):
        # 坐标x
        self.id = _id
        self.x = x
        # 坐标y
        self.y = y
        # 单个兴趣点要收集的数据量
        self.data = 2


# 计算需要收集的数据总量
def calculate_data(points):
    all_data = 0
    for point in points:
        all_data += point.data
    return all_data


# 产生兴趣点集合
def generate_points(num, x_max, y_max, data_max):
    points = []
    for i in range(num):
        x = random.randint(0, x_max)
        y = random.randint(0, y_max)
        data = random.randint(1, data_max)
        point = Point(i, x, y, data)
        points.append(point)
    return points


if __name__ == '__main__':
    point_list = generate_points(100, 100, 100, 3)

    # x = map(lambda point: point.x, point_list)
    # y = map(lambda point: point.y, point_list)
    #
    # fig = plt.figure(figsize=(10, 10))
    # ax = fig.gca()
    # ax.set_xticks(np.arange(0, 101, 5))
    # ax.set_yticks(np.arange(0, 101, 5))
    # plt.scatter(list(x), list(y))
    # plt.grid(True)
    # plt.rc('grid', linestyle="-", color='black')
    #
    # plt.show()
