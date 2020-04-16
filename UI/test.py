# import tkinter as tk
# import time
# import threading as th
#
#
# def click():
#     global str1
#     str1.set(1)
#
#
# def fun(a):
#     i = 100 ** 2
#     while i > 0:
#         i -= 1
#         global str1
#         str1.set(i)
#         print(a)
#
#
# root = tk.Tk()
# str1 = tk.Variable()
# str1.set('123')
# lb = tk.Label(root, textvariable=str1)
# lb.pack()
# btn = tk.Button(root, text='hit', command=click)
# btn.pack()
# t1 = th.Thread(target=fun(1), args=(13,))
# t1.start()
# time.sleep(2)
# t2 = th.Thread(target=fun(2), args=(14,))
# t2.start()
# root.mainloop()
import time
import tkinter
import requests
import threading
import random


def getPrice():
    price = random.randint(1, 5)
    return price


root = tkinter.Tk()
label1 = tkinter.Label(root, text='init...')
label1.pack()


def threadGetPrice():
    while True:
        t1 = 3
        while t1 > 0:
            t1 -= 1
            label1['text'] = getPrice()
            time.sleep(1)

        if t1 == 0:
            print('over')
            break


t = threading.Thread(target=threadGetPrice, args=(), name='thread-refresh')
t.setDaemon(True)
t.start()

root.mainloop()
