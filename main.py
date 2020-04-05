import Task
import User
import random
import numpy as np
import math
import Paint

# 兴趣点x轴最大范围
P_X_MAX = 100
# 兴趣点y轴最大范围
P_Y_MAX = 100
# 兴趣点个数
P_NUM = 100
# 兴趣点最大数据量
P_DATA_MAX = 3

# 待选集最大人员数
C_NUM_MAX = 40
# 感知任务时间T
T = 17
# 感知任务预算B
B = 1000
# 感知任务兴趣点集合
P = Task.generate_points(P_NUM, P_X_MAX, P_Y_MAX, P_DATA_MAX)
# 感知任务
task = Task.Task(T, B, P)

# 高信誉贡献高质量数据概率
alpha = 0.5
# 低信誉贡献高质量数据概率
beta = 0.5
# 选择参与者集合的平均信誉
average_credit = 0

# 信誉在[0,0.3)之间贡献高质量感知数据的概率
p_low = 0.3
# 信誉在[0.3,0.6)之间贡献高质量感知数据的概率
p_medium = 0.5
# 信誉在[0.6,1)之间贡献高质量感知数据的概率
p_high = 0.8


def online_quality_aware(time, budget, data):
    # 阈值
    delta_threshold = data / budget
    # 时间阶段
    t = 1
    # 记录的所有参与者
    m_all_p = User.generate_candidate(C_NUM_MAX, task, P_X_MAX, P_Y_MAX)
    # 感知任务待选集合
    m_candidate = []
    # 感知任务参与者选择集合
    m_selected = []
    # 一次感知任务中所有参与者集合
    m_all_selected = []

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

        # Paint.paint_dot(task, m_selected, P_X_MAX, P_Y_MAX)
        # 模拟被选择参与者执行任务,返回离开者集合
        m_departure = run_task(m_selected, t)
        m_all_selected.extend(m_departure)

        # 离开的参与者任务完成情况计算
        for m in m_departure:
            actual_value = 0
            for p in m.actual_points:
                actual_value += p.data
            pre_value = utility_function(m_all_selected + [m]) - utility_function(m_all_selected)
            # 实际完成的任务情况低于预估的情况
            if actual_value < pre_value:
                # 回报扣除
                r_f = m.reward * (pre_value - actual_value) / pre_value
                m.reward -= r_f
                budget += r_f
                print('reward deduct')

        rate = task_complete_level()
        print('t=', t, "%.4f" % rate, budget, len(m_selected), len(m_all_selected),
              'average_credit=%s' % average_credit, delta_threshold)
        delta_threshold = TSM(m_departure, m_all_selected, budget, delta_threshold)

        if delta_threshold <= 0:
            m_all_selected.extend(m_selected)
            m_selected.clear()
            break
        t += 1


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
                if m.credit >= average_credit:
                    e_p += 1 * alpha
                else:
                    e_p += 1 * beta
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
    if t == 17:
        m_departure.extend(m_selected)
        m_selected.clear()
    for m in m_selected:
        # 用户已完成全部兴趣点的感知，用户离开
        if len(m.interest_points) == 0:
            m_departure.append(m)
            print('\tid=%s complete leave' % m.id)
            break
        # 产生一个随机数，模拟用户随机离开，当前设置概率为0.2
        ran = random.random()
        if ran >= 0.1 or t == 1:
            # 在每一轮的时间里，一个参与者随机完成1-5个兴趣点的任务
            count = random.randint(1, 3)
            count = min(count, len(m.interest_points))
            for i in range(count):
                # 每次随机选取一个随机兴趣点
                index = random.randint(0, len(m.interest_points) - 1)
                p = m.interest_points[index]
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
                # 从该用户感兴趣点集合中移除
                m.interest_points.remove(p)

        else:
            print('\tid=%s halfway leave' % m.id)
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
    average_rate = 0

    for m in m_all_selected:
        rate = individual_level(m)
        average_rate += rate

    average_rate = average_rate / len(m_all_selected)
    global average_credit

    # 所有参与者的报酬总和
    actual_reward = 0

    # 高信誉完成任务情况大于平均人数
    alpha_num = 0
    # 低信誉完成任务情况大于平均人数
    beta_num = 0

    for m in m_departure:
        individual_rate = individual_level(m)
        if m.credit >= average_credit:
            if individual_rate >= average_rate:
                alpha_num += 1
        else:
            if individual_rate >= average_rate:
                beta_num += 1

        actual_reward += m.reward
        # 个人信誉更新函数
        r_m = 0.5 * (4 / np.pi) * np.arctan((individual_rate - average_rate) / (average_rate + 0.00001))
        tmp = m.credit + r_m
        tmp = min(1, tmp)
        tmp = max(-1, tmp)
        m.credit = (1 / np.pi) * np.arcsin(tmp) + 0.5

    # 平均信誉值更新
    # average_credit = sum(list(map(lambda x: x.credit, m_departure))) / len(m_departure)

    if actual_reward <= 0:
        k = 1
    else:
        k = (actual_utility_f(m_departure) - utility_function(m_departure)) / actual_reward

    global alpha, beta
    alpha = alpha_num / len(m_departure)
    beta = beta_num / len(m_departure)

    actual_data = 0
    for i in task.actual_points:
        actual_data += i

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
    req = np.array([1 for _ in range(len(m.actual_points) + len(m.interest_points))])
    act = np.array(list(map(lambda x: min(x.data, 1), m.actual_points)) + len(m.interest_points) * [0])
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
    online_quality_aware(17, 200, task.data)
    print(list(map(lambda x: x.data, task.points)))
    print(task.actual_points)
    # u = User.add_new_user()
    # u.interest_points = Task.generate_points(5, P_X_MAX, P_Y_MAX, P_DATA_MAX)
    #
    # M = run_task([u])
