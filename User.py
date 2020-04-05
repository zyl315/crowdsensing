import MySQLdb
import uuid as uid
import random
import Task
import math
import copy

# 连接数据库
db = MySQLdb.connect("localhost", "root", "root", "crowdsensing", charset='utf8')


# 参与者类
class User:
    # 参与者感知的兴趣点集合
    interest_points = []
    # 参与者实际完成的兴趣点
    actual_points = []
    # 参与者未完成的兴趣点
    unfinished_points = []
    # 参与者要求感知任务的报酬
    reward = 0
    # 参与者位置
    position = (0, 0)

    def __init__(self, _id, uuid, credit):
        self.id = _id
        self.uuid = uuid
        self.credit = credit
        self.interest_points = list()
        self.actual_points = list()
        self.unfinished_points = list()


# 参与位置
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# 从数据库中获取所有历史参与者信息
def get_all_user():
    users = []
    sql = "select * from user "
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            users.append(User(result[0], result[1], result[2]))
    except:
        print("error:unable to fetch data")

    return users


# 关闭数据库连接
def db_close():
    db.close()


# 往数据库添加参与者
def insert_user(user):
    sql = "insert into user(uuid,credit) value('%s', %s)" % (user.uuid, user.credit)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except AttributeError:
        db.rowback()
        print("error: insert user fail")


# 更新用户信息
def update_user(uuid, credit):
    sql = "update user set credit = %s where uuid = %s" % (credit, uuid)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rowback()
        print("error: update user fail")


# 模拟新的用户到达,并且初始化信誉值为0.5
def add_new_user():
    _uuid = uid.uuid1().hex
    user = User(None, _uuid, credit=0.5)
    insert_user(user)
    return user


# 产生感知任务参与者的候选集
def generate_candidate(num, task, x_max, y_max, pb=0.1):
    m_candidate = []

    # 从数据库获得所有的历史参与者
    user_from_database = get_all_user()

    for i in range(num):

        if len(user_from_database) == 0:
            break
        index = random.randint(0, len(user_from_database) - 1)
        u = user_from_database[index]
        user_from_database.remove(u)

        length = len(task.points) - 1
        # 模拟参与者请求的感知兴趣点集合，随机选择

        num = random.randint(1, 20)
        # for p in task.points:
        #     dis = math.sqrt((p.x - u.position[0]) ** 2 + (p.y - u.position[1] ** 2))
        #     if dis < 10:
        #         u.interest_points.append(p)
        # print(len(u.interest_points))
        u.interest_points = random.sample(task.points, num)

        # 模拟参与者提出感知的报酬,随机给出
        u.reward = random.randint(1, 10)

        # 模拟参与者随机位置
        x = random.randint(0, x_max)
        y = random.randint(0, y_max)
        u.position = (x, y)
        m_candidate.append(u)

    return m_candidate


if __name__ == '__main__':
    points = Task.generate_points(10, 100, 100, 2)
    # task = Task.Task(17, 1000, points)
    # candidate = generate_candidate(100, task)
    # for p in candidate:
    #     print(p.uuid, p.credit, p.interest_points, p.reward)
    #
    # for _ in range(100):
    #     generate_candidate(10,task)
