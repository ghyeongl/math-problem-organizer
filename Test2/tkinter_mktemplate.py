import json
import os
import shutil
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
from Tests import pdf_convert
import time


class SrcCanvas(Canvas):
    def __init__(self, parent, scrollbar, path):
        self.master1 = parent
        self.width = 1000
        self.image = self._set_image(path)
        Canvas.__init__(self, parent, width=self.image.width, height=self.image.height, cursor="cross",
                        scrollregion=(0, 0, self.image.width, self.image.height))

        self.x = self.y = 0
        self.path = path

        self.image_id = None
        self.image_tk = None
        self.draw = ImageDraw.Draw(self.image)
        self.scroll = scrollbar
        self.pack(side="top", fill="both", expand=True)
        self.bind("<ButtonPress-1>", self.on_button_press)
        self.bind("<B1-Motion>", self.on_move_press)
        self.bind("<ButtonRelease-1>", self.on_button_release)
        self.bind_all("<MouseWheel>", self._on_mousewheel)
        self.bind_all("<Up>", self._arrow_up)
        self.bind_all("<Down>", self._arrow_down)

        self.rect = None

        self.start_x = None
        self.start_y = None

        self.stack = []
        self.redoStack = []
        self.rectStack = []
        self.redoRectStack = []

        self._draw_image()

    def _arrow_up(self, event):
        self.yview_scroll(-1, "units")

    def _arrow_down(self, event):
        self.yview_scroll(1, "units")

    def _on_mousewheel(self, event):
        self.yview_scroll(-1 * event.delta, "units")

    def _set_image(self, path):
        self.image = Image.open(path)
        self._resize()
        return self.image

    def _draw_image(self):
        self.image_tk = ImageTk.PhotoImage(image=self.image)
        self.image_id = self.create_image(0, 0, anchor="nw", image=self.image_tk)
        self._redraw()
        self.stack.append(self.image.copy())

    def on_button_press(self, event):
        self.redoStack = []
        self.start_x = event.x - 5
        self.start_y = event.y + self.scroll.get()[0] * self.image.height - 5

        self.rect = self.create_rectangle(self.x, self.y, 1, 1, fill="", outline="red")

    def on_move_press(self, event):
        curX, curY = (event.x - 5, event.y + self.scroll.get()[0] * self.image.height - 5)

        self.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        curX, curY = (event.x - 5, event.y + self.scroll.get()[0] * self.image.height - 5)
        if curX > self.image.width:
            curX = self.image.width
        if curY > self.image.height:
            curY = self.image.height
        self.draw.rectangle((self.start_x, self.start_y, curX, curY), outline=(0, 255, 0), width=3)
        data = ((int(self.start_x), int(self.start_y)), (int(curX), int(curY)), (self.image.width, self.image.height))
        self.rectStack.append(data)
        self._redraw()
        self.delete(self.rect)

    def undo(self):
        if len(self.stack) > 1:
            self.stack.pop()
            self.redoStack.append(self.image.copy())
            self.image = self.stack.pop()
            self.redoRectStack.append(self.rectStack.pop())
            self._redraw()
            self.master1.master0.a0.a4.configure(state="normal")

    def redo(self):
        if len(self.redoStack) > 0:
            self.image = self.redoStack.pop()
            self.rectStack.append(self.redoRectStack.pop())
            self._redraw()
        else:
            self.master1.master0.a0.a4.configure(state="disabled")

    # def zoom_in(self):
    #     self.width += 100
    #     self._resize()
    #     self._redraw()
    #
    # def zoom_out(self):
    #     self.width -= 100
    #     self._resize()
    #     self._redraw()

    def _redraw(self):
        self.image_tk = ImageTk.PhotoImage(image=self.image)
        self.itemconfig(self.image_id, image=self.image_tk)
        self.draw = ImageDraw.Draw(self.image)
        self.image.save(self.path, "JPEG")
        self.stack.append(self.image.copy())

    def _resize(self):
        w, h = self.image.size
        if self.width > 0:
            self.image = self.image.resize((self.width, int(self.width * h / w)), Image.ANTIALIAS)

    def change_zoom(self):
        if self.width == 1000:
            self.width = 500
        else:
            self.width = 1000

        self._resize()
        self._redraw()
        self.configure(scrollregion=(0, 0, self.image.width, self.image.height))


class CanvasHandler(Frame):
    def __init__(self, master1, scroller, **kw):
        super().__init__(**kw)
        self.master1 = master1
        self.scroller = scroller
        self.canvas = None

        self.interface = self.InterfaceH(self)
        self.file = self.FileH(self)
        self.pages = self.PagesH(self)
        self.page = self.PageH(self)
        self.data = self.DataH(self)

        self.bind_all("<Left>", self.pages.prevPage)
        self.bind_all("<Right>", self.pages.nextPage)

    # 전체적인 in out 을 관리하는 역할
    class InterfaceH:
        def __init__(self, master2):
            self.master2 = master2

        def importFile(self):
            self.master2.pagesH.destroy()
            if self.master2.fileH.importFile():
                self.master2.fileH.makeImages()
                self.master2.pagesH.setFromFile()
                self.setLocation(self.master2.fileH.fileH)
                self.setScale(self.master2.pagesH.amount)
            else:
                pass

        def saveTemplate(self):
            pass

        def setScale(self, amount):
            self.master2.master1.master0.b0.b1.configure(to=amount)

        def setScaleStatus(self, current):
            self.master2.master1.master0.b0.b1.set(current)

        def setLocation(self, file):
            self.master2.master1.master0.a0.a2.configure(text=file)

        def nextPageEvent(self, event):
            self.master2.pagesH.nextPage()

        def prevPageEvent(self, event):
            self.master2.pagesH.prevPage()

        def reset(self):
            self.master2.fileH.reset()
            self.master2.pagesH.reset()

        def templateReset(self):
            self.master2.pagesH.reset()
            self.master2.fileH.reset()
            self.master2.dataH.reset()

        def saveData(self):
            self.master2.dataH.save()

    # 파일을 관리하는 역할
    class FileH:
        def __init__(self, master2):
            self.master2 = master2
            self.file = ""
            self.imgPath = ""
            self.imgNum = 0

        def importFile(self):
            self.master2.interfaceH.reset()
            self.file = filedialog.askopenfilename(
                initialdir="/", title="Select fileH", filetypes=(("pdf files", "*.pdf"),))
            return self.isImported()

        def isImported(self):
            return self.file != ''

        def makeImages(self):
            self._cleanupTemp()
            file_name = self._convertToImg()
            self.imgPath = f"../Exports/Temp/{file_name}"
            self.imgNum = len(os.listdir(self.imgPath))

        def _cleanupTemp(self):
            shutil.rmtree(f"../Exports/Temp")
            os.mkdir(f"../Exports/Temp")
            self.imgPath = ""
            self.imgNum = 0

        def _convertToImg(self):
            totalPages = pdf_convert.getPageAmount(self.file)

            file_name = self.file.split("/")[-1].split(".")[0]
            while os.path.exists(f"../Exports/Temp/{file_name}"):
                file_name = file_name + "1"
            os.mkdir(f"../Exports/Temp/{file_name}")

            threadList = []
            before = time.time()
            self.master2.master1.master0.setTitle(f": Converting...")
            for i in range(1, totalPages + 1, 50):
                lastPage = i + 49 if i + 49 < totalPages else totalPages

                t = pdf_convert.PdfConverter(self.file, file_name, i, lastPage)
                threadList.append(t)
                t.start()
                if len(threadList) == 8:
                    for t in threadList:
                        t.join()
                    threadList = []

            for t in threadList:
                t.join()

            print("All threads finished")
            print("time: " + round(time.time() - before, 1).__str__())

            self.master2.master1.master0.setTitle(": Finished")
            return file_name

        def reset(self):
            self.__init__(self.master2)

    # 전체 페이지의 생성, 삭제, 보기를 관리하는 역할
    class PagesH:
        def __init__(self, master2):
            self.master2 = master2

            self.file = None
            self.amount = 1
            self.pageNum = self.PageNum(self, 1)

        class PageNum:
            def __init__(self, master3, amount: int):
                self.master3 = master3
                self._current = 1
                self.amount = amount

            def getCurrent(self) -> int:
                return self._current

            def setCurrent(self, current: int) -> int:
                self.master3.master2.dataH.save(self._current)
                if 1 <= int(current) <= int(self.amount):
                    self._current = int(current)
                return self._current

        def setFromFile(self):
            self.file = self.master2.fileH
            self.amount = self.file.imgNum
            self.pageNum = self.PageNum(self, self.amount)
            self.setPage()

        def destroy(self):
            if self.master2.canvas is not None:
                self.master2.dataH.save(self.pageNum.getCurrent())
            self.reset()

        def setPage(self, page=None):
            if page is not None:
                self.pageNum.setCurrent(page)
            self.master2.pageH.setCanvas(f"{self.file.imgPath}/{self.pageNum.getCurrent()}.jpg")

        def nextPage(self):
            current = self.pageNum.getCurrent()
            if current >= self.amount:
                return
            self.master2.interfaceH.setScaleBarStatus(current + 1)

        def prevPage(self):
            current = self.pageNum.getCurrent()
            if current < 2:
                return
            self.master2.interfaceH.setScaleBarStatus(current - 1)

        def reset(self):
            self.master2.pageH.reset()
            self.__init__(self.master2)
            self.master2.interfaceH.setScaleBarStatus(self.pageNum.getCurrent())
            self.master2.interfaceH.setScaleBar(self.amount)

    # 페이지의 수정, 보기 변환, 실행 취소 등을 관리하는 역할
    class PageH:
        def __init__(self, master2):
            self.master2 = master2
            self.scroller = self.master2.scroller

        def setCanvas(self, path):
            self.reset()
            self.master2.canvas = SrcCanvas(self.master2.master1, self.scroller, path)
            self.scroller.config(command=self.master2.canvas.yview)
            self.master2.canvas.config(yscrollcommand=self.scroller.set)
            # CanvasH 에 의해 Encapsulated 되어있음
            self.master2.canvas.pack()

        def undo(self):
            if self.master2.canvas is not None:
                self.master2.canvas.undo()

        def redo(self):
            if self.master2.canvas is not None:
                self.master2.canvas.redo()

        def changeZoom(self):
            if self.master2.canvas is not None:
                self.master2.canvas.changeZoom()
                self.scroller.config(command=self.master2.canvas.yview)
                self.master2.canvas.config(yscrollcommand=self.scroller.set)

        def reset(self):
            if self.master2.canvas is not None:
                self.master2.canvas.destroy()
                self.master2.canvas = None

    # 데이터의 초기화, 저장을 관리하는 역할
    class DataH:
        def __init__(self, master2):
            self.master2 = master2
            self.datafile = "../Data/templates.json"

            self.templateName = None
            self.file = None
            self.pageNum = None
            self.canvas = None
            self._resetArgs()

            self.data = self.placeJson()

        def save(self, current=None):
            self._resetArgs()
            self.structData()
            if current is None:
                current = self.master2.pagesH.pageNum.getCurrent()
            if self.master2.canvas is not None:
                for item in self.master2.canvas.rectStack:
                    self.data[self.templateName][self.file][str(current)].append(item)
                self._dumpJson()
            else:
                pass

        def reset(self):
            self._resetArgs()
            self.placeJson()
            self.structData()
            self.data[self.templateName] = {}
            self._dumpJson()

        def structData(self):
            # 템플릿이 존재하지 않는 경우
            if not self.data.get(self.templateName):
                self.data[self.templateName] = {}
            # 파일명이 존재하지 않는 경우
            if self.file not in self.data[self.templateName]:
                self.data[self.templateName][self.file] = {}
            # 페이지 번호가 존재하지 않는 경우
            if str(self.pageNum.getCurrent()) not in self.data[self.templateName][self.file]:
                self.data[self.templateName][self.file][str(self.pageNum.getCurrent())] = []

        def placeJson(self):
            if os.path.exists(self.datafile):
                self.data = self._loadJson()
            else:
                self.data = self._initJson()
            return self.data

        def _initJson(self):
            json.dump({}, open(self.datafile, "w"), indent=2)
            with open(self.datafile, "r") as f:
                d = f.read()
            return json.loads(d)

        def _loadJson(self):
            with open(self.datafile, "r") as f:
                d = f.read()
                if d == "":
                    return self._initJson()
                return json.loads(d)

        def _dumpJson(self):
            with open(self.datafile, "w") as f:
                json.dump(self.data, f, indent=2, sort_keys=True, ensure_ascii=False)

        def _resetArgs(self):
            self.templateName = self.master2.master1.master0.templateName
            self.file = self.master2.fileH.fileH
            self.pageNum = self.master2.pagesH.pageNum
            self.canvas = self.master2.canvas


class Window(Tk):
    def __init__(self):
        super().__init__()
        self.templateName = "Sample Template"
        self.setTitle()

        self.c0 = self.ColumnC(self)
        self.a0 = self.ColumnA(self, self.c0.canvasH)
        self.b0 = self.ColumnB(self, self.c0.canvasH)

        self._packFrames()
        self._configWindow()

    class ColumnA(Frame):
        def __init__(self, master0, canvasH: CanvasHandler):
            super().__init__(master0)
            self.config(width=1000, height=100)
            self.a1 = Button(self, text="파일 불러오기", command=canvasH.interface.importFile)
            self.a2 = Label(self, text="파일 위치", width=70)
            self.a3 = Button(self, text="실행 취소", command=canvasH.page.undo)
            self.a4 = Button(self, text="다시 실행", command=canvasH.page.redo)
            self.a5 = Button(self, text="보기 변경", command=canvasH.page.changeZoom)
            self.a6 = Button(self, text="템플릿 리셋", command=canvasH.interface.templateReset)
            self.a1.grid(row=0, column=0)
            self.a2.grid(row=0, column=1)
            self.a3.grid(row=0, column=2)
            self.a4.grid(row=0, column=3)
            self.a5.grid(row=0, column=4)
            self.a6.grid(row=0, column=5)

    class ColumnB(Frame):
        def __init__(self, master0, canvasH: CanvasHandler):
            super().__init__(master0)
            self.config(width=1000, height=100)
            self.b1 = Scale(self, from_=1, to=canvasH.pages.amount, orient=HORIZONTAL,
                            length=1000, command=canvasH.pages.setPage)
            self.b2 = Button(self, text="이전 페이지", command=canvasH.pages.prevPage)
            self.b3 = Button(self, text="다음 페이지", command=canvasH.pages.nextPage)
            self.b1.grid(row=0, column=0)
            self.b2.grid(row=0, column=1)
            self.b3.grid(row=0, column=2)

            self.bind_all("<Left>", canvasH.interface.prevPageEvent)
            self.bind_all("<Right>", canvasH.interface.nextPageEvent)

    class ColumnC(Frame):
        def __init__(self, master0):
            super().__init__(master0)
            self.master0 = master0
            self.config(width=1500, height=800)
            self.vbar = Scrollbar(self, orient=VERTICAL)
            self.canvasH = CanvasHandler(self, self.vbar)
            self.test = Label(self, text="test", background="green")
            self.vbar.pack(side=RIGHT, fill=Y)
            self.canvasH.pack(side=LEFT, fill=BOTH, expand=True)

    def _packFrames(self):
        self.a0.pack(side=TOP, fill=Y)
        self.b0.pack(side=TOP, fill=Y)
        self.c0.pack(expand=True, fill=BOTH)

    def _setActionOnClose(self):
        self.c0.canvasH.interface.saveData()
        self.destroy()

    def setTitle(self, value=None):
        if value is None:
            self.title(f"Template maker : {self.templateName}")
        else:
            self.title(f"Template maker : {self.templateName} {value}")

    def _configWindow(self):
        self.protocol("WM_DELETE_WINDOW", self._setActionOnClose)
        self.mainloop()


window = Window()
