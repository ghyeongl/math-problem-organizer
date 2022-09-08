from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw

from Refractor1.classes.coord import Coord
from Refractor1.classes.template import Template


# 한 페이지를 할당하는 캔버스를 관리
class PageOnCanvas(Canvas):
    def __init__(self, chiefClass, template):
        self.chiefClass = chiefClass
        self.template = template
        if self.template.imagePainter is None:
            raise Exception("Image Painter is not loaded")

        # Set Dependency
        self.canvasArea = self.chiefClass.c0
        self.scroller = self.chiefClass.c0.vbar

        self.width, self.height = self.template.imagePainter.getWidth(), self.template.imagePainter.getHeight()
        super().__init__(master=self.canvasArea, width=self.width, height=self.height, cursor="cross",
                         scrollregion=(0, 0, self.width, self.height))

        self.imageId = None
        self.imageTk = None

        self.pack(side="top", fill="both", expand=True)
        self.bind("<ButtonPress-1>", self.on_button_press)
        self.bind("<B1-Motion>", self.on_move_press)
        self.bind("<ButtonRelease-1>", self.on_button_release)
        self.bind_all("<MouseWheel>", self._on_mousewheel)
        self.bind_all("<Up>", self._arrow_up)
        self.bind_all("<Down>", self._arrow_down)

        self.rect = None
        self.start = Coord(w=self.width, h=self.height)
        self.end = Coord(w=self.width, h=self.height)

        self.updateCanvas()

    # 이미지가 변경될 때
    def updateCanvas(self):
        self.imageTk = ImageTk.PhotoImage(image=self.template.imagePainter.image)
        self._loadOrUpdateImage(self.imageTk)
        self.configure(scrollregion=(0, 0, self.template.getWidth(), self.template.getHeight()))

    def on_button_press(self, event):
        self.start.setCoord(event.x - 5, event.y + self.scroller.get()[0] * self.template.getHeight() - 5)
        self.rect = self.create_rectangle(self.start.x, self.start.y, self.start.x, self.start.y, fill="",
                                          outline="red")

    def on_move_press(self, event):
        current = Coord(event.x - 5, event.y + self.scroller.get()[0] * self.template.getHeight() - 5)
        self.coords(self.rect, self.start.x, self.start.y, current.x, current.y)

    def on_button_release(self, event):
        self.end.setCoord(event.x - 5, event.y + self.scroller.get()[0] * self.template.getHeight() - 5)
        self.end.x = self.template.getWidth() if self.end.x > self.template.getWidth() else self.end.x
        self.end.y = self.template.getHeight() if self.end.y > self.template.getHeight() else self.end.y
        self.template.addRectangle(self.start, self.end)
        self.updateCanvas()
        self.delete(self.rect)

    def changeSize(self):
        self.template.changeImageSize()
        self.updateCanvas()

    def _loadOrUpdateImage(self, imageTk):
        if self.imageId is None:
            self.imageId = self.create_image(0, 0, anchor="nw", image=imageTk)
        else:
            self.itemconfig(self.imageId, image=imageTk)

    def _arrow_up(self, event):
        self.yview_scroll(-1, "units")

    def _arrow_down(self, event):
        self.yview_scroll(1, "units")

    def _on_mousewheel(self, event):
        self.yview_scroll(-1 * event.delta, "units")


class CanvasHandler(Frame):
    def __init__(self, chiefClass, templateName, **kw):
        super().__init__(**kw)
        self.chiefClass = chiefClass  # CanvasHandler should be intend Tkinter class
        self.templateName = templateName
        self.template = Template(self.templateName)

        self.configurator = self.Configurator(self.chiefClass, self.template)
        self.controller = self.Controller(self.chiefClass, self.template, self.configurator)

        self.bind_all("<Left>", self.controller.prevPage)
        self.bind_all("<Right>", self.controller.nextPage)

    class Controller:
        def __init__(self, chiefClass, template, configurator):
            self.chiefClass = chiefClass
            self.template = template
            self.configurator = configurator

        def importFile(self):
            file = filedialog.askopenfilename(
                initialdir="/", title="Select fileH", filetypes=(("pdf files", "*.pdf"),))
            self.template.setFile(file)
            if self.template.fileHandler.checkFileImported():
                self.configurator.initFile()

        def setScaleBarStatus(self, current):
            self.chiefClass.b0.b1.set(current)

        # 페이지 설정 관련
        def setPage(self, page):
            self.template.setPage(page)
            return self.configurator.loadCanvas()

        def nextPage(self):
            self.template.nextPage()
            self.configurator.updateScaleBar()
            return self.configurator.loadCanvas()

        def prevPage(self):
            self.template.prevPage()
            self.configurator.updateScaleBar()
            return self.configurator.loadCanvas()

        def nextPageEvent(self, event):
            self.nextPage()

        def prevPageEvent(self, event):
            self.prevPage()

        # 상태 설정 관련
        def undo(self):
            if self.configurator.canvas is None:
                return False
            self.template.undo()
            self.configurator.updateCanvas()
            return True

        def redo(self):
            if self.configurator.canvas is None:
                return False
            self.template.redo()
            self.configurator.updateCanvas()
            return True

        def changeSize(self):
            self.template.changeImageSize()
            self.configurator.updateCanvas()

        def saveTemplate(self):
            self.template.save()

    class Configurator:
        def __init__(self, chiefClass, template):
            self.chiefClass = chiefClass
            self.template = template

            self.scaleBarWidget = None
            self.fileLocationWidget = None
            self.scrollerWidget = None

            self.canvas = None

        def lateInitVariables(self):
            self.scaleBarWidget = self.chiefClass.b0.b1
            self.fileLocationWidget = self.chiefClass.a0.a2
            self.scrollerWidget = self.chiefClass.c0.vbar

        # 스케일바 크기 설정
        def setScaleBar(self, amount):
            self.scaleBarWidget.configure(to=amount)

        # 위젯에 파일 경로 표시
        def setLocation(self, file):
            self.fileLocationWidget.configure(text=file)

        # 캔버스 설정
        def loadCanvas(self):
            self.unloadCanvas()
            if not self.template.fileHandler.checkFileImported():
                return False
            self.canvas = PageOnCanvas(self.chiefClass, self.template)
            self.scrollerWidget.config(command=self.canvas.yview)
            self.canvas.config(yscrollcommand=self.scrollerWidget.set)
            return True

        def unloadCanvas(self):
            if self.canvas is not None:
                self.canvas.destroy()
                # self.canvas = None
                return True
            return False

        def updateCanvas(self):
            self.canvas.updateCanvas()

        def updateScaleBar(self):
            self.scaleBarWidget.set(self.template.currentPage)

        def initFile(self):
            self.template.setPage(1)
            self.loadCanvas()
            self.setScaleBar(self.template.getTotalPage())
            self.setLocation(self.template.fileHandler.filePath)
            self.template.setPage(1)


class MakeTemplateWindow(Toplevel):
    def __init__(self, master, templateName):
        super().__init__(master)

        self.c0 = self.ColumnC(self, templateName)
        self.a0 = self.ColumnA(self, self.c0.canvasH)
        self.b0 = self.ColumnB(self, self.c0.canvasH)
        self.c0.canvasH.configurator.lateInitVariables()

        self.setTitle()
        self._packFrames()
        self._configWindow()

    class ColumnA(Frame):
        def __init__(self, master0, canvasH: CanvasHandler):
            super().__init__(master0)
            self.config(width=1000, height=100)
            self.a1 = Button(self, text="파일 불러오기", command=canvasH.controller.importFile)
            self.a2 = Label(self, text="파일 위치", width=70)
            self.a3 = Button(self, text="실행 취소", command=canvasH.controller.undo)
            self.a4 = Button(self, text="다시 실행", command=canvasH.controller.redo)
            self.a5 = Button(self, text="보기 변경", command=canvasH.controller.changeSize)
            self.a1.grid(row=0, column=0)
            self.a2.grid(row=0, column=1)
            self.a3.grid(row=0, column=2)
            self.a4.grid(row=0, column=3)
            self.a5.grid(row=0, column=4)

    class ColumnB(Frame):
        def __init__(self, master0, canvasH: CanvasHandler):
            super().__init__(master0)
            self.config(width=1000, height=100)
            self.b1 = Scale(self, from_=1, to=canvasH.template.fileHandler.totalPage, orient=HORIZONTAL,
                            length=1000, command=canvasH.controller.setPage)
            self.b2 = Button(self, text="이전 페이지", command=canvasH.controller.prevPage)
            self.b3 = Button(self, text="다음 페이지", command=canvasH.controller.nextPage)
            self.b1.grid(row=0, column=0)
            self.b2.grid(row=0, column=1)
            self.b3.grid(row=0, column=2)

            self.bind_all("<Left>", canvasH.controller.prevPageEvent)
            self.bind_all("<Right>", canvasH.controller.nextPageEvent)

    class ColumnC(Frame):
        def __init__(self, master0, templateName):
            super().__init__(master0)
            self.master0 = master0
            self.config(width=1500, height=800)
            self.vbar = Scrollbar(self, orient=VERTICAL)
            self.canvasH = CanvasHandler(self.master0, templateName)
            self.test = Label(self, text="test", background="green")
            self.vbar.pack(side=RIGHT, fill=Y)
            self.canvasH.pack(side=LEFT, fill=BOTH, expand=True)

    def _packFrames(self):
        self.a0.pack(side=TOP, fill=Y)
        self.b0.pack(side=TOP, fill=Y)
        self.c0.pack(expand=True, fill=BOTH)

    def _setActionOnClose(self):
        self.c0.canvasH.controller.saveTemplate()
        self.destroy()

    def setTitle(self, value=None):
        print(self.c0.canvasH.templateName)
        if value is None:
            self.title(f"Template maker : {self.c0.canvasH.templateName}")
        else:
            self.title(f"Template maker : {self.c0.canvasH.templateName} {value}")

    def _configWindow(self):
        self.protocol("WM_DELETE_WINDOW", self._setActionOnClose)
        self.mainloop()


if __name__ == "__main__":
    window = MakeTemplateWindow()
