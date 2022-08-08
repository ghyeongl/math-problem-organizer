import json
import os
import shutil
from tkinter import *
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk, ImageDraw
from Tests import pdf_convert


class SrcCanvas(Canvas):
    def __init__(self, parent, scrollbar, path):
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
        source = cv2.imread(path)
        image = cv2.cvtColor(source, cv2.COLOR_BGR2RGB)
        self.image = Image.fromarray(image)
        self._resize()
        return self.image

    def _draw_image(self):
        self.image_tk = ImageTk.PhotoImage(image=self.image)
        self.image_id = self.create_image(0, 0, anchor="nw", image=self.image_tk)
        self._redraw()
        self.stack.append(self.image.copy())

    def on_button_press(self, event):
        self.redoStack = []
        self.start_x = event.x
        self.start_y = event.y + self.scroll.get()[0] * self.image.height

        self.rect = self.create_rectangle(self.x, self.y, 1, 1, fill="", outline="red")

    def on_move_press(self, event):
        curX, curY = (event.x, event.y + self.scroll.get()[0] * self.image.height)

        self.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        curX, curY = (event.x, event.y + self.scroll.get()[0] * self.image.height)
        self.draw.rectangle((self.start_x, self.start_y, curX, curY), outline=(0, 255, 0), width=3)
        self.rectStack.append((self.start_x, self.start_y, curX, curY))
        self._redraw()
        self.delete(self.rect)

    def undo(self):
        if len(self.stack) > 1:
            self.stack.pop()
            self.redoStack.append(self.image.copy())
            self.image = self.stack.pop()
            self.redoRectStack.append(self.rectStack.pop())
            self._redraw()
            a4.configure(state="normal")

    def redo(self):
        if len(self.redoStack) > 0:
            print(self.redoStack)
            self.image = self.redoStack.pop()
            self.rectStack.append(self.redoRectStack.pop())
            self._redraw()
        else:
            a4.configure(state="disabled")

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


class CanvasHandler:
    def __init__(self, frame, scroll):
        self.frame = frame
        self.scroll = scroll
        self.file = None
        self.imgPath = None

        self.current = 1
        self.amount = None
        self.canvas = None
        self.data = []

    def select_file(self):
        global b1

        if self.canvas is not None:
            self.save_data()
            self.canvas.destroy()

        self.__init__(self.frame, self.scroll)

        self.file = filedialog.askopenfilename(initialdir="/", title="Select file",
                                               filetypes=(("pdf files", "*.pdf"),))
        print("file: " + self.file)
        if self.file == "":
            return

        shutil.rmtree(f"../Exports/")
        os.mkdir(f"../Exports/")
        a2.configure(text=self.file)
        self.make_page()
        b1.configure(to=self.amount)

        self._init_canvas()

    def make_page(self):
        identifier = pdf_convert.pdfToImg(self.file)
        self.imgPath = f"../Exports/{identifier}"
        self.amount = len(os.listdir(self.imgPath))

    def next_page(self):
        if self.current >= self.amount:
            return
        b1.set(self.current + 1)

    def prev_page(self):
        if self.current < 2:
            return
        b1.set(self.current - 1)

    def next_page_event(self, event):
        self.next_page()

    def prev_page_event(self, event):
        self.prev_page()

    def _set_page(self, pageNum):
        if pageNum is None:
            return
        pageNum = int(pageNum)
        if pageNum > self.amount or pageNum < 1:
            print("page out of bound")
            return
        self.current = pageNum
        self._init_canvas()

    def set_page_event(self, pageNum):
        self.save_data()
        self.current = pageNum
        self._set_page(pageNum)

    def _init_canvas(self):
        if self.canvas is not None:
            self.canvas.destroy()
        self.canvas = SrcCanvas(self.frame, self.scroll, f"{self.imgPath}/{self.current}.jpg")
        self.scroll.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scroll.set)
        self.canvas.pack(side=LEFT, expand=True, fill=BOTH)

    def canvas_undo(self):
        if self.canvas is not None:
            self.canvas.undo()

    def canvas_redo(self):
        if self.canvas is not None:
           self.canvas.redo()

    def change_zoom(self):
        self.canvas.change_zoom()
        self.scroll.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scroll.set)

    def save_data(self):
        if not os.path.exists("../Data/templates.json"):
            with open("../Data/templates.json", "w") as f:
                json.dump({}, f)

        with open("../Data/templates.json", "r") as f:
            d = f.read()
        if not d == "":
            data = json.loads(d)
        else:
            with open("../Data/templates.json", "w") as f:
                data = {}
                json.dump({}, f)

        if not data.get(templateName):
            data[templateName] = {}
        if self.file not in data[templateName]:
            data[templateName][self.file] = {}
        if str(self.current) not in data[templateName][self.file]:
            data[templateName][self.file][str(self.current)] = []
        for item in self.canvas.rectStack:
            data[templateName][self.file][str(self.current)].append(item)
        with open("../Data/templates.json", "w") as f:
            json.dump(data, f, indent=2)

    def template_reset(self):
        with open("../Data/templates.json", "r") as f:
            d = f.read()
        data = json.loads(d)
        data[templateName] = {}
        with open("../Data/templates.json", "w") as f:
            json.dump(data, f, indent=2)
        self.canvas.destroy()
        self.__init__(self.frame, self.scroll)


window = Tk()
templateName = "Sample Template"
window.title(f"Template maker: {templateName}")

c0 = Frame(window, width=1500, height=800)

# 우측 조절 바
vbar = Scrollbar(c0, orient=VERTICAL)
vbar.pack(side=RIGHT, fill=Y)

# 캔버스 설정
canvasH = CanvasHandler(c0, vbar)

# 캔버스 핸들러
c0.bind_all("<Left>", canvasH.prev_page)
c0.bind_all("<Right>", canvasH.next_page)

a0 = Frame(window)
a1 = Button(a0, text="파일 불러오기", command=canvasH.select_file)
a2 = Label(a0, text="파일 위치", width=70)
a3 = Button(a0, text="실행 취소", command=canvasH.canvas_undo)
a4 = Button(a0, text="다시 실행", command=canvasH.canvas_redo)
a5 = Button(a0, text="보기 변경", command=canvasH.change_zoom)
a6 = Button(a0, text="템플릿 리셋", command=canvasH.template_reset)
a1.grid(row=0, column=0)
a2.grid(row=0, column=1)
a3.grid(row=0, column=2)
a4.grid(row=0, column=3)
a5.grid(row=0, column=4)
a6.grid(row=0, column=5)


b0 = Frame(window)
b1 = Scale(b0, from_=1, to=canvasH.amount, orient=HORIZONTAL, length=1000, command=canvasH.set_page_event)
b2 = Button(b0, text="이전 페이지", command=canvasH.prev_page)
b3 = Button(b0, text="다음 페이지", command=canvasH.next_page)
b1.grid(row=0, column=0)
b2.grid(row=0, column=1)
b3.grid(row=0, column=2)

a0.pack(side=TOP, fill='y')
b0.pack(side=TOP, fill='y')
c0.pack(expand=True, fill=BOTH)

window.mainloop()
