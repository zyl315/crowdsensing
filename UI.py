import tkinter as tk
from tkinter import Label

import main as m
import threading
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Application:
    def __init__(self):
        self.T = 0
        self.budget = 0
        self.p_num = 0
        self.c_num = 0
        self.root = None
        self.top = None
        self._round = 1

        self.title_info = None
        self.list_box1 = None
        self.list_box2 = None
        self.frame_r = None
        self.fig = None
        self.can = None
        self.img_label = None

        self.ans = None

    def create_main_window(self):
        self.root = tk.Tk()
        self.root.title('参数设置')
        self.root.geometry('320x200')

        # 感知轮数
        l1 = tk.Label(self.root, text='轮数:')
        l1.place(x=70, y=20, height=20, width=30)
        text1 = tk.Variable()
        text1.set(3)
        inp1 = tk.Entry(self.root, textvariable=text1)
        inp1.place(x=110, y=20, height=20, width=120)

        # 感知预算
        l2 = tk.Label(self.root, text='预算:')
        l2.place(x=70, y=45, height=20, width=30)
        text2 = tk.Variable()
        text2.set(200)
        inp2 = tk.Entry(self.root, textvariable=text2)
        inp2.place(x=110, y=45, height=20, width=120)

        # 兴趣点数
        l3 = tk.Label(self.root, text='兴趣点数:')
        l3.place(x=50, y=70, height=20, width=50)
        text3 = tk.Variable()
        text3.set(100)
        inp3 = tk.Entry(self.root, textvariable=text3)
        inp3.place(x=110, y=70, height=20, width=120)

        # 最大感知人数
        l4 = tk.Label(self.root, text='最大感知人数:')
        l4.place(x=25, y=95, height=20, width=75)
        text4 = tk.Variable()
        text4.set(40)
        inp4 = tk.Entry(self.root, textvariable=text4)
        inp4.place(x=110, y=95, height=20, width=120)

        def click():
            self.T = int(text1.get())
            self.budget = int(text2.get())
            self.p_num = int(text3.get())
            self.c_num = int(text4.get())

            t1 = threading.Thread(target=self.begin_sensing(), args=(), name='thread-refresh')
            t1.setDaemon(True)
            t1.start()
            self.create_sub_window()

        # 确认感知
        btn = tk.Button(self.root, text='开始感知', command=click)
        btn.place(x=140, y=130)

    def create_sub_window(self):
        top = tk.Toplevel()
        self.top = top
        top.title('感知过程')
        top.geometry('690x530')
        top.resizable(0, 0)

        self.update_data()
        # 左边视图
        frame_l = tk.LabelFrame(self.top, relief='groove')
        frame_l.pack(side='left', fill='y')

        lb1 = tk.Label(frame_l, text="参与用户集", relief='groove')
        lb1.pack(fill='x')

        # 左边上表格标题
        title1 = tk.Label(frame_l, text='id\t信誉\t报酬', relief='groove')
        title1.pack(fill='x')
        # 左边上表格
        l_box1 = tk.Listbox(frame_l, width='25', height='11', listvariable=self.list_box1)
        l_box1.pack(fill='both')

        lb2 = tk.Label(frame_l, text="离开用户集", relief='groove')
        lb2.pack(fill='x')
        # 左边下表格标题
        title2 = tk.Label(frame_l, text='id\t信誉\t报酬', relief='groove')
        title2.pack(fill='x')
        # 左边下表格
        l_box2 = tk.Listbox(frame_l, width='25', height='15', relief='groove', listvariable=self.list_box2)
        l_box2.pack(fill='both')

        frame_r = tk.LabelFrame(self.top, relief='groove')
        frame_r.pack(side='left', fill='y')
        self.frame_r = frame_r

        frame_title = tk.LabelFrame(frame_r, relief='groove')
        frame_title.pack(side='top', fill='x')

        def add():
            if self._round < self.T:
                self._round += 1
            self.update_data()

        def sub():
            if self._round > 1:
                self._round -= 1
            self.update_data()

        btn1 = tk.Button(frame_title, text='<', command=sub)
        btn1.pack(side='left')

        lb3 = tk.Label(frame_title, textvariable=self.title_info, width='65')
        lb3.pack(side='left')

        btn1 = tk.Button(frame_title, text='>', command=add)
        btn1.pack(side='right')

        global img_png, img
        img = Image.open('img/%s.png' % self._round)
        img_png = ImageTk.PhotoImage(img)
        lb4 = tk.Label(frame_r, image=img_png)
        self.img_label = lb4
        lb4.pack(fill='both', expand=1)

        # self.can = tk.Canvas()
        # self.can = FigureCanvasTkAgg(self.fig, frame_r)
        # self.can.draw()
        # self.can.get_tk_widget().pack(fill='both', expand=1)

        # im = tk.PhotoImage(self.fig)

        self.top.after(500)

    def begin_sensing(self):
        self.ans = m.init(self.T, self.budget, self.p_num, self.c_num)

    def update_data(self):
        _round = self._round
        t = self.ans[_round][0]
        rate = self.ans[_round][1]
        budget = self.ans[_round][2]
        m_selected = self.ans[_round][3]
        m_all_selected = self.ans[_round][4]
        self.fig = self.ans[_round][5]

        # 更新标题
        if self.title_info is None:
            self.title_info = tk.Variable()
        self.title_info.set("当前轮数:%s/%s\t当前用户数:%s\t任务完成度:%.1f%%\t预算剩余:%.2f" % (
            t, self.T, len(m_selected), rate * 100, budget))

        # 更新表格1
        l_box1 = list()
        if self.list_box1 is None:
            self.list_box1 = tk.Variable()
        for item in sorted(m_selected, key=lambda m: m.id):
            str_1 = "%6s%16s%12s" % (item.id, round(item.credit, 2), round(item.reward, 2))
            l_box1.append(str_1)
        self.list_box1.set(tuple(l_box1))

        # 更新表格2
        l_box2 = list()
        if self.list_box2 is None:
            self.list_box2 = tk.Variable()
        for item in sorted(m_all_selected, key=lambda m: m.id):
            str_1 = "%6s%16s%12s" % (item.id, round(item.credit, 2), round(item.reward, 2))
            l_box2.append(str_1)
        self.list_box2.set(tuple(l_box2))

        # 更新图片
        if self.img_label is not None:
            global img_png, img
            img = Image.open('img/%s.png' % self._round)
            img_png = ImageTk.PhotoImage(img)
            self.img_label.configure(image=img_png)

    def begin(self):
        self.create_main_window()
        self.root.mainloop()


def destroy(self):
    self.root.destory()


if __name__ == '__main__':
    app = Application()
    app.begin()
