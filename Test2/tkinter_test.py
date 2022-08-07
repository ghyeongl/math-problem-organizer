from tkinter import *
import tkinter.ttk as ttk


window = Tk()
window.title("Practice Management")
window.geometry('610x150')


a1 = Label(window, text="스냅샷 선택", width=10)
values = [str(i)+"번" for i in range(1, 101)]
a2 = ttk.Combobox(window, values=values, state="readonly", width=30)
a3 = Button(window, text="스냅샷 만들기", width=20)
a1.grid(row=0, column=0)
a2.grid(row=0, column=1)
a3.grid(row=0, column=2)

b1 = Label(window, text="학생 선택", width=10)
b2 = ttk.Combobox(window, values=values, state="readonly", width=30)
b3 = Button(window, text="학생 만들기", width=20)
b1.grid(row=1, column=0)
b2.grid(row=1, column=1)
b3.grid(row=1, column=2)

c1 = Label(window, text="템플릿 선택", width=10)
c2 = ttk.Combobox(window, values=values, state="readonly", width=30)
c3 = Button(window, text="템플릿 만들기", width=20)
c1.grid(row=2, column=0)
c2.grid(row=2, column=1)
c3.grid(row=2, column=2)

d1 = Label(window, text="오답 선택", width=10)
d2 = ttk.Combobox(window, values=values, state="readonly", width=30)
d3 = Button(window, text="오답 만들기", width=20)
d1.grid(row=3, column=0)
d2.grid(row=3, column=1)
d3.grid(row=3, column=2)

e1 = Button(window, text="페이지 제작")
e1.grid(row=4, column=0, columnspan=3)

window.mainloop()
