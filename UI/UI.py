import tkinter as tk
from main import *


def main_page():
    root = tk.Tk()
    root.title('参数设置')
    root.geometry('320x200')

    # 感知轮数
    l1 = tk.Label(root, text='轮数:')
    l1.place(x=70, y=20, height=20, width=30)
    text1 = tk.Variable()
    text1.set(30)
    inp1 = tk.Entry(root, textvariable=text1)
    inp1.place(x=110, y=20, height=20, width=120)

    # 感知预算
    l2 = tk.Label(root, text='预算:')
    l2.place(x=70, y=45, height=20, width=30)
    text2 = tk.Variable()
    text2.set(200)
    inp2 = tk.Entry(root, textvariable=text2)
    inp2.place(x=110, y=45, height=20, width=120)

    # 兴趣点数
    l3 = tk.Label(root, text='兴趣点数:')
    l3.place(x=50, y=70, height=20, width=50)
    text3 = tk.Variable()
    text3.set(100)
    inp3 = tk.Entry(root, textvariable=text3)
    inp3.place(x=110, y=70, height=20, width=120)

    # 最大感知人数
    l4 = tk.Label(root, text='最大感知人数:')
    l4.place(x=25, y=95, height=20, width=75)
    text4 = tk.Variable()
    text4.set(40)
    inp4 = tk.Entry(root, textvariable=text4)
    inp4.place(x=110, y=95, height=20, width=120)

    def begin_sensing():
        time = int(text1.get())
        budget = int(text2.get())
        p_num = int(text3.get())
        c_num = int(text4.get())
        print(time, budget, p_num, c_num)
        top = tk.Toplevel()
        top.title('感知过程')
        top.geometry('690x510')
        top.resizable(0, 0)
        init(time, budget, p_num, c_num, top)

    # 确认感知
    btn = tk.Button(root, text='开始感知', command=begin_sensing)
    btn.place(x=140, y=130)

    root.mainloop()


def show_window(top, m_selected, m_all_selected, task, t, T, budget, rate):
    frame_l = tk.LabelFrame(top, relief='groove')
    frame_l.pack(side='left', fill='y')

    lb1 = tk.Label(frame_l, text="参与用户", relief='groove')
    lb1.pack(fill='x')

    # 左边上表格标题
    title1 = tk.Label(frame_l, text='id\t信誉\t报酬', relief='groove')
    title1.pack(fill='x')
    # 左边上表格
    l_box1 = tk.Listbox(frame_l, width='25', height='11')
    l_box1.pack(fill='both')
    for item in m_selected:
        str_1 = "%6s%16s%12s" % (item.id, item.credit, item.reward)
        l_box1.insert('end', str_1)

    lb2 = tk.Label(frame_l, text="全部用户", relief='groove')
    lb2.pack(fill='x')
    # 左边上表格标题
    title2 = tk.Label(frame_l, text='id\t信誉\t报酬', relief='groove')
    title2.pack(fill='x')
    # 左边上表格
    l_box2 = tk.Listbox(frame_l, width='25', height='15', relief='groove')
    l_box2.pack(fill='both')
    for item in m_all_selected:
        str_2 = "%6s%16s%12s" % (item.id, item.credit, item.reward)
        l_box2.insert('end', str_2)

    frame_r = tk.LabelFrame(top, relief='groove')
    frame_r.pack(side='left', fill='y')
    title_info = "当前轮数:%s/%s\t当前用户数:%s\t任务完成度:%s\t预算剩余:%s" % (t, T, len(m_selected), rate, budget)
    lb3 = tk.Label(frame_r, text=title_info, relief='groove')
    lb3.pack(fill='both')

    global img
    img = tk.PhotoImage(file="E:/Users/HP/PycharmProjects/crowdsensing/img/1.png")
    lb4 = tk.Label(frame_r, image=img)
    lb4.pack(fill='both', expand=1)


if __name__ == '__main__':
    main_page()
