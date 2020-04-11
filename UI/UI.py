import tkinter
from main import *


def main_page():
    root = tkinter.Tk()
    root.title('参数设置')
    root.geometry('320x200')

    # 感知轮数
    l1 = tkinter.Label(root, text='轮数:')
    l1.place(x=70, y=20, height=20, width=30)
    text1 = tkinter.Variable()
    text1.set(30)
    inp1 = tkinter.Entry(root, textvariable=text1)
    inp1.place(x=110, y=20, height=20, width=120)

    # 感知预算
    l2 = tkinter.Label(root, text='预算:')
    l2.place(x=70, y=45, height=20, width=30)
    text2 = tkinter.Variable()
    text2.set(200)
    inp2 = tkinter.Entry(root, textvariable=text2)
    inp2.place(x=110, y=45, height=20, width=120)

    # 兴趣点数
    l3 = tkinter.Label(root, text='兴趣点数:')
    l3.place(x=50, y=70, height=20, width=50)
    text3 = tkinter.Variable()
    text3.set(100)
    inp3 = tkinter.Entry(root, textvariable=text3)
    inp3.place(x=110, y=70, height=20, width=120)

    # 最大感知人数
    l4 = tkinter.Label(root, text='最大感知人数:')
    l4.place(x=25, y=95, height=20, width=75)
    text4 = tkinter.Variable()
    text4.set(40)
    inp4 = tkinter.Entry(root, textvariable=text4)
    inp4.place(x=110, y=95, height=20, width=120)

    def begin_sensing():
        time = int(text1.get())
        budget = int(text2.get())
        p_num = int(text3.get())
        c_num = int(text4.get())
        print(time, budget, p_num, c_num)
        # init(time, budget, p_num, c_num)

    # 确认感知
    btn = tkinter.Button(root, text='开始感知', command=begin_sensing)
    btn.place(x=140, y=130)

    root.mainloop()


if __name__ == '__main__':
    main_page()
