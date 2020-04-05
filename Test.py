import random
import numpy as np


class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age


u1 = [User(1, 22), User(2, 23)]
u2 = [User(3, 24)]


# print(u1 + u2)

# _list = [1, 2, 3, 4, 5, 6]
# for i in range(5):
#     print(random.sample(_list, 3))
#     print(_list)


def frobenius_norm():
    c = [2, 2, 2, 2, 2, 2]
    A = np.array(list(map(lambda x: x + 0, c)))
    B = np.array([0, 0, 0, 0, 0, 0])

    print(1 - cal_F(A - B) / cal_F(A))


def cal_F(A):
    ans = 0
    for i in A:
        ans += i ** 2
    return np.sqrt(ans)


def func1():
    a = [i for i in range(10)]
    b = []
    print(a, b)
    for i in range(3):
        b.append(a[i])
        a.remove(a[i])
    print(a, b)

    # frobenius_norm()
    # func1()


credit = (1 / np.pi) * np.arcsin(min(0.5 + (0.05409469707308279 - 0.05427744571733659) / 0.05427744571733659, 1)) + 0.5

print(credit)
