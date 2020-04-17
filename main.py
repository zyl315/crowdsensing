import Task
import User
import random
import numpy as np
import UI
import Paint
import time as times
import copy

# 兴趣点x轴最大范围
P_X_MAX = 100
# 兴趣点y轴最大范围
P_Y_MAX = 100
# # 兴趣点个数
# P_NUM = 100
# 兴趣点最大数据量
P_DATA_MAX = 2

# # 待选集最大人员数
# C_NUM_MAX = 40
# 感知任务时间T
T = 0
# # 感知任务预算B
# B = 200
# # 感知任务兴趣点集合
# P = Task.generate_points(P_NUM, P_X_MAX, P_Y_MAX, P_DATA_MAX)
# 感知任务
task = None
# 平均信誉
average_credit = 0

# 界面显示
result_dict = dict()


def begin():
    app = UI.Application()
    app.begin()
    print()


def init(t, b, p_num, c_num_max):
    global task, T
    p = Task.generate_points(p_num, P_X_MAX, P_Y_MAX, P_DATA_MAX)
    T = t
    task = Task.Task(t, b, p)
    res = online_quality_aware(t, b, task.data, c_num_max)
    return res


def online_quality_aware(time, budget, data, c_num):
    # 阈值
    delta_threshold = data / budget
    # 时间阶段
    t = 1
    # 记录的所有参与者
    m_all_p = User.generate_candidate(c_num, task, P_X_MAX, P_Y_MAX)
    # 感知任务待选集合
    m_candidate = []
    # 感知任务参与者选择集合
    m_selected = []
    # 一次感知任务中所有参与者集合
    m_all_selected = []

    print('m_all_p %s' % len(m_all_p))

    while t <= time:
        # 新到达的参与者
        m_arrive = add_new_arrive(m_all_p)
        # t时刻到达的参与者添加进M_candidate
        m_candidate.extend(m_arrive)
        # 计算平均信誉
        calculate_average_credit(m_candidate + m_selected + m_all_selected)
        # 参与者选择
        while len(m_candidate) != 0:
            # 选择出边际效应最大的候选者
            m = arg_max(m_candidate, m_all_selected)
            # 预估该参与者的单位价格的数据量
            value = (utility_function(m_all_selected + [m]) - utility_function(m_all_selected)) / m.reward
            # 该参与者满足阈值并且预算没有耗尽
            if delta_threshold <= value and budget > m.reward:
                m_selected.append(m)
                budget -= m.reward
            else:
                m_all_p.append(m)
            # 将该参与者添加进被选择集，移出待选集合
            m_candidate.remove(m)

        img = Paint.paint_dot(task, m_selected, P_X_MAX, P_Y_MAX, t)
        # 模拟被选择参与者执行任务,返回离开者集合

        rate = task_complete_level()
        print('t=%s' % t, "rate=%.4f" % rate, 'budget=%s' % budget, 'remain=%s' % len(m_selected),
              'leave=%s' % len(m_all_selected), 'δ=%s' % delta_threshold)
        result_dict[t] = [t, rate, budget, m_selected.copy(), m_all_selected.copy(), img]

        # 模拟参与者执行任务
        m_departure = run_task(m_selected, t)
        m_all_selected.extend(m_departure)

        # 阈值更新
        delta_threshold = TSM(m_departure, m_all_selected, budget, delta_threshold)
        # 数据收集完成
        if delta_threshold <= 0:
            m_all_selected.extend(m_selected)
            m_selected.clear()
            break
        t += 1
    return result_dict


# 添加新的参与者
def add_new_arrive(m_all_p):
    arrive = random.sample(m_all_p, random.randint(0, len(m_all_p)))
    for m in arrive:
        m_all_p.remove(m)
    return arrive


def arg_max(m_candidate, m_all_selected):
    m_max = 0
    value = 0
    for i in range(len(m_candidate)):
        v = utility_function(m_all_selected + [m_candidate[i]]) - utility_function(m_all_selected)
        if v > value:
            value = v
            m_max = i
    return m_candidate[m_max]


# 计算边际效用函数
def utility_function(M):
    ans = 0
    for p in task.points:
        e_p = 0
        for m in M:
            if p in m.interest_points:
                e_p += 1 * np.sin(np.pi * 0.5 * m.credit)
        ans += min(p.data, e_p)
    return ans


# 计算候选集合的平均信誉
def calculate_average_credit(m_candidate):
    credit = 0
    for m in m_candidate:
        credit += m.credit
    global average_credit
    average_credit = credit / len(m_candidate)


# 计算集合中信誉大于平均信誉人数的概率
def cal_g_ave_c_num(m_candidate):
    num = 0
    for m in m_candidate:
        if m.credit > average_credit:
            num += 1
    global pr
    pr = num / len(m_candidate)
    return pr


# 模拟被选择的参与者执行任务
def run_task(m_selected, t):
    m_departure = list()
    if t == T:
        m_departure.extend(m_selected)
        m_selected.clear()
    for m in m_selected:
        # 用户已完成全部兴趣点的感知，用户离开
        if len(m.unfinished_points) == 0:
            m_departure.append(m)
            print('\tid=%s reward=%s complete leave' % (m.id, m.reward))
            break
        # 产生一个随机数，模拟用户随机离开，当前设置概率为0.2
        ran = random.random()
        if ran >= 0.1 or t == 1:
            # 在每一轮的时间里，一个参与者随机完成1-5个兴趣点的任务
            count = random.randint(1, 3)
            count = min(count, len(m.unfinished_points))
            for i in range(count):
                # 每次随机选取一个随机兴趣点
                index = random.randint(0, len(m.unfinished_points) - 1)
                p = m.unfinished_points[index]
                # 参与者与兴趣点的位置
                distance = np.sqrt((m.position[0] - p.x) ** 2 + (
                        m.position[1] - p.y) ** 2)
                # 模拟随机是否能在该兴趣点完成任务
                ran = random.random()
                if ran <= m.credit:
                    # 完成该兴趣点数据收集
                    task.actual_points[p.id] += 1
                # 模拟用户到达该兴趣点,用户位置更新
                m.position = (p.x, p.y)
                # # 添加到用户实际完成的兴趣点
                m.actual_points.append(Task.Point(p.id, p.x, p.y, p.data))
                # 从该用户未完成的兴趣点集合中移除
                m.unfinished_points.remove(p)

        else:
            print('\tid=%s reward=%s halfway leave' % (m.id, m.reward))
            # 添加到任务离开者结合
            m_departure.append(m)
            # 模拟用户中途离开任务
    for m in m_departure:
        if m in m_selected:
            m_selected.remove(m)

    return m_departure


# F范数
def cal_F(A):
    ans = 0
    for i in A:
        ans += i ** 2
    return np.sqrt(ans)


# 阈值和信誉更新函数
def TSM(m_departure, m_all_selected, budget, delta_threshold):
    # complete_rate = task_complete_level()
    if len(m_departure) == 0:
        return delta_threshold

    for m in m_all_selected:
        rate = individual_level(m)

    global average_credit

    # 所有参与者的报酬总和
    actual_reward = 0

    for m in m_departure:
        actual_value = 0
        for _ in m.actual_points:
            actual_value += 1
        pre_value = utility_function(m_all_selected + [m]) - utility_function(m_all_selected)
        # 实际完成的任务情况低于预估的情况
        if actual_value < pre_value:
            # 回报扣除
            r_f = m.reward * (pre_value - actual_value) / pre_value
            m.reward -= r_f
            budget += r_f
            print('\tid=%s reward deduct.' % m.id)

        # 个人信誉更新函数
        # r_m = min(0.5 * (4 / np.pi) * np.arctan((actual_value - pre_value) / (pre_value + 0.000000000001)), 0)
        tmp = m.credit + min((actual_value - pre_value) / (pre_value + 0.000000000001), 0)
        tmp = min(1, tmp)
        tmp = max(-1, tmp)
        m_credit = (1 / np.pi) * np.arcsin(tmp) + 0.5

        # User.update_user(m.uuid, m_credit)

        actual_reward += m.reward
        print('\tid=%s,credit=%.4f, reward=%.4f,rate=%.4f' %
              (m.id, m_credit, m.reward, individual_level(m)))

    if actual_reward == 0:
        k = 0
    else:
        k = (actual_utility_f(m_departure) - utility_function(m_departure)) / actual_reward
    print('\tk=%s' % k)

    actual_data = 0
    for i in task.actual_points:
        actual_data += min(i, 2)

    new_delta_threshold = (1.1 ** k) * ((task.data - actual_data) / budget)

    return new_delta_threshold


# 计算整体任务完成情况
def task_complete_level():
    request = np.array([2 for _ in range(len(task.points))])
    actual = np.array(list(map(lambda x: min(x, 2), task.actual_points)))
    complete_rate = 1 - cal_F(request - actual) / cal_F(request)
    return complete_rate


# 计算个人任务完成情况
def individual_level(m):
    req = np.array([1 for _ in range(len(m.interest_points))])
    act = np.array(list(map(lambda x: min(x.data, 1), m.actual_points)) + len(m.unfinished_points) * [0])
    rate = 1 - cal_F(req - act) / cal_F(req)
    return rate


# 实际完成效应
def actual_utility_f(M):
    actual_utility = 0
    for m in M:
        for p in m.actual_points:
            actual_utility += p.data

    return actual_utility


if __name__ == '__main__':
    begin()
