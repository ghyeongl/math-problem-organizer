from tkinter import *
import tkinter.ttk as ttk

from Refractor1.classes.program_data import ProgramData
from Codes.Classes import DataAccessLayer
from Codes.Classes.curent_settings import CurrentSettings
from Codes.Classes import SnapshotServiceLayer
from Codes.Classes import TemplateModifier


class Window(Tk):
    def __init__(self):
        super().__init__()

        self.title("Practice Management")
        self.geometry('610x150')


        self.currentSettings = CurrentSettings()
        self.snapshotService = SnapshotServiceLayer()
        self.templateService = TemplateModifier()
        self.a0 = self.ColumnA(self.snapshotService.getSnapshotsList(), self.currentSettings)
        self.b0 = self.ColumnB(self.programData)
        self.c0 = self.ColumnC(self.programData)
        self.d0 = self.ColumnD(self.programData)
        self.e0 = self.ColumnE(self.programData)

        self._packFrames()
        self._configWindow()

    class ColumnA(Frame):
        def __init__(self, snapshotsList, setSnapshotName):
            super().__init__()
            a1 = Label(self, text="스냅샷 선택", width=10)
            a2 = ttk.Combobox(self, values=snapshotsList, state="readonly", width=30)
            a2.bind("<<ComboboxSelected>>", lambda event: setSnapshotName(a2.get()))
            a3 = Button(self, text="스냅샷 만들기", width=20, command=None)
            a1.grid(row=0, column=0)
            a2.grid(row=0, column=1)
            a3.grid(row=0, column=2)

    class ColumnB(Frame):
        def __init__(self, master, programData):
            self.master = master
            super().__init__()
            self.b1 = Label(self, text="학생 선택", width=10)
            self.b2 = ttk.Combobox(self, values=programData.getStudents(), state="readonly", width=30)
            self.b3 = Button(self, text="학생 만들기", width=20, command=self.master.addStudent)
            self.b1.grid(row=0, column=0)
            self.b2.grid(row=0, column=1)
            self.b3.grid(row=0, column=2)
            self.b2.bind("<<ComboboxSelected>>", self.master.whenStudentSelected)

    class ColumnC(Frame):
        def __init__(self, master, programData):
            self.master = master
            super().__init__()
            self.c1 = Label(self, text="템플릿 선택", width=10)
            self.c2 = ttk.Combobox(self, values=programData.getTemplates(), state="readonly", width=30)
            self.c3 = Button(self, text="템플릿 만들기", width=20, command=self.master.addTemplate)
            self.c1.grid(row=0, column=0)
            self.c2.grid(row=0, column=1)
            self.c3.grid(row=0, column=2)
            self.c2.bind("<<ComboboxSelected>>", self.master.whenTemplateSelected)

    class ColumnD(Frame):
        def __init__(self, master, programData):
            self.master = master
            super().__init__()
            self.d1 = Label(self, text="오답 선택", width=10)
            self.d2 = ttk.Combobox(self, values=programData.getIncorrect(), state="readonly", width=30)
            self.d3 = Button(self, text="오답 만들기", width=20)
            self.d1.grid(row=0, column=0)
            self.d2.grid(row=0, column=1)
            self.d3.grid(row=0, column=2)

    class ColumnE(Frame):
        def __init__(self, master, programData):
            self.master = master
            super().__init__()
            self.e1 = Button(self, text="페이지 제작")
            self.e1.grid(row=0, column=0, columnspan=3)

    def _packFrames(self):
        self.a0.pack(side=TOP, fill=Y)
        self.b0.pack(side=TOP, fill=Y)
        self.c0.pack(side=TOP, fill=Y)
        self.d0.pack(side=TOP, fill=Y)
        self.e0.pack(side=TOP, fill=Y)

    def whenSnapshotSelected(self, event):
        snapshot = event.widget.get()
        self.programData.setCurrentSnapshot(snapshot)
        self.programData.setDataBySnapshot()
        self.b0.b2.config(values=self.programData.getStudents())
        self.c0.c2.config(values=self.programData.getTemplates())

    def whenStudentSelected(self, event):
        student = event.widget.get()
        self.programData.setCurrentStudent(student)
        self.d0.d2.config(values=self.programData.getIncorrect())

    def whenTemplateSelected(self, event):
        template = event.widget.get()
        if template == "<새로 만들기>":
            template = ""
            self.c0.c2.set("")
        self.programData.setCurrentTemplate(template)
        self.programData.setIncorrectByData()

    def addSnapshot(self):
        self.programData.addSnapshot()
        self.a0.a2.config(values=self.programData.getSnapshots())

    def addStudent(self):
        self.programData.addStudent()
        self.b0.b2.config(values=self.programData.getStudents())

    def addTemplate(self):
        title = self.c0.c2.get()
        if title == "<새로 만들기>":
            self.c0.c2.config(values=self.programData.getTemplates())
        self.configTemplateWindow = ConfigTemplateWindow(self, self.programData, title)

    def _configWindow(self):
        self.mainloop()

    def setSnapshotName(self, snapshotName):
        self.currentSettings.setSnapshotName(snapshotName)



if __name__ == "__main__":
    window = Window()
