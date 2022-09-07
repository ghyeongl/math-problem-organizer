from tkinter import *
import tkinter.ttk as ttk

from Refractor1.classes.program_data import ProgramData


class Window(Tk):
    def __init__(self):
        super().__init__()

        self.title("Practice Management")
        self.geometry('610x150')

        self.programData = ProgramData()
        self.a0 = self.ColumnA(self.programData)
        self.b0 = self.ColumnB(self.programData)
        self.c0 = self.ColumnC(self.programData)
        self.d0 = self.ColumnD(self.programData)
        self.e0 = self.ColumnE(self.programData)

        self._packFrames()
        self._configWindow()

    class ColumnA(Frame):
        def __init__(self, programData):
            super().__init__()
            a1 = Label(self, text="스냅샷 선택", width=10)
            a2 = ttk.Combobox(self, values=programData.getSnapshotsList(), state="readonly", width=30)
            a3 = Button(self, text="스냅샷 만들기", width=20)
            a1.grid(row=0, column=0)
            a2.grid(row=0, column=1)
            a3.grid(row=0, column=2)

    class ColumnB(Frame):
        def __init__(self, programData):
            super().__init__()
            b1 = Label(self, text="학생 선택", width=10)
            b2 = ttk.Combobox(self, values=programData.getStudentsList(), state="readonly", width=30)
            b3 = Button(self, text="학생 만들기", width=20)
            b1.grid(row=0, column=0)
            b2.grid(row=0, column=1)
            b3.grid(row=0, column=2)

    class ColumnC(Frame):
        def __init__(self, programData):
            super().__init__()
            c1 = Label(self, text="템플릿 선택", width=10)
            c2 = ttk.Combobox(self, values=programData.getTemplatesList(), state="readonly", width=30)
            c3 = Button(self, text="템플릿 만들기", width=20)
            c1.grid(row=0, column=0)
            c2.grid(row=0, column=1)
            c3.grid(row=0, column=2)

    class ColumnD(Frame):
        def __init__(self, programData):
            super().__init__()
            d1 = Label(self, text="오답 선택", width=10)
            d2 = ttk.Combobox(self, values=programData.getIncorrectList(), state="readonly", width=30)
            d3 = Button(self, text="오답 만들기", width=20)
            d1.grid(row=0, column=0)
            d2.grid(row=0, column=1)
            d3.grid(row=0, column=2)

    class ColumnE(Frame):
        def __init__(self, programData):
            super().__init__()
            e1 = Button(self, text="페이지 제작")
            e1.grid(row=0, column=0, columnspan=3)

    def _packFrames(self):
        self.a0.pack(side=TOP, fill=Y)
        self.b0.pack(side=TOP, fill=Y)
        self.c0.pack(side=TOP, fill=Y)
        self.d0.pack(side=TOP, fill=Y)
        self.e0.pack(side=TOP, fill=Y)

    def _configWindow(self):
        self.mainloop()


window = Window()
