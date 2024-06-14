from tkinter import *

from Codes.View.make_template import MakeTemplateWindow


class ConfigHandler:
    def __init__(self):
        self.templateName = None


class ConfigTemplateWindow(Toplevel):
    def __init__(self, master, programData, status=""):
        super().__init__(master)
        self.mainPage = master
        self.programData = programData
        self.configH = ConfigHandler()
        self.titleStatus = status

        self.title("템플릿 설정")
        self.geometry('610x150')

        self.a0 = self.ColumnA(self)
        self.b0 = self.ColumnB(self)
        self.c0 = self.ColumnC(self)

        self.makeTemplateWindow = None

        self._packFrames()
        self._configWindow()

    class ColumnA(Frame):
        def __init__(self, master):
            self.master = master
            super().__init__(master)
            self.a1 = Label(self, text="템플릿 제목", width=10)
            print(self.master.titleStatus)
            if self.master.titleStatus != "":
                self.a2 = Entry(self, width=30)
                self.a2.insert(0, self.master.titleStatus)
                self.a2.config(state="readonly")
                self.a3 = Button(self, text="제목 입력하기", width=20, state="disabled")
            else:
                self.a2 = Entry(self, width=30)
                self.a3 = Button(self, text="제목 입력하기", width=20, command=self.master.whenTitleEntered)
            self.a1.grid(row=0, column=0)
            self.a2.grid(row=0, column=1)
            self.a3.grid(row=0, column=2)

    class ColumnB(Frame):
        def __init__(self, master):
            self.master = master
            super().__init__(master)
            self.b1 = Label(self, text="문제 리스트", width=10)
            self.b2 = Listbox(self, width=30, height=5)
            self.b31 = Button(self, text="위로 올리기", width=20, state="disabled")
            self.b32 = Button(self, text="아래로 내리기", width=20, state="disabled")
            self.b33 = Button(self, text="삭제", width=20, state="disabled")
            self.b1.grid(row=0, column=0, rowspan=3)
            self.b2.grid(row=0, column=1, rowspan=3)
            self.b31.grid(row=0, column=2)
            self.b32.grid(row=1, column=2)
            self.b33.grid(row=2, column=2)

    class ColumnC(Frame):
        def __init__(self, master):
            super().__init__(master)
            self.c1 = Button(self, text="템플릿 편집하기", command=self.master.whenTemplateEditClicked)
            if self.master.titleStatus == "":
                self.c1.config(state="disabled")
            self.c1.grid(row=0, column=0, columnspan=3)

    def whenTemplateEditClicked(self):
        if self.titleStatus != "":
            self.configH.templateName = self.titleStatus
        self.makeTemplateWindow = MakeTemplateWindow(self, self.configH.templateName)

    def whenTitleEntered(self):
        self.configH.templateName = self.a0.a2.get()
        if self.configH.templateName in self.programData.getTemplates():
            return False
        self.a0.a2.config(state="readonly")
        self.a0.a3.config(state="disabled")
        self.c0.c1.config(state="normal")
        self.programData.appendTemplate(self.configH.templateName)

    def _packFrames(self):
        self.a0.pack()
        self.b0.pack()
        self.c0.pack()

    def _configWindow(self):
        self.mainloop()
