# 显示手柄和分割线
from tkinter import *

m1 = PanedWindow(sashrelief=SUNKEN, height=480, width=480)  # 默认是左右分布的
m1.pack(fill=BOTH, expand=1)

left = Label(m1, text='left pane')
m1.add(left)

m2 = PanedWindow(orient=VERTICAL, sashrelief=SUNKEN)
m1.add(m2)

top = Label(m2, text='top pane')
m2.add(top)

bottom = Label(m2, text='bottom pane')
m2.add(bottom)

mainloop()
