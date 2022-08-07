from tkinter import *
import cv2
import imutils
import tkinter.ttk as ttk
from PIL import Image, ImageTk

x, y = 0, 0
rect = None
start_x = None
start_y = None


class SrcCanvas(Canvas):
    def __init__(self, parent, image, scrollbar):
        Canvas.__init__(self, parent, width=image.width, height=image.height, cursor="cross",
                        scrollregion=(0, 0, image.width, image.height))

        self.x = self.y = 0
        self.image = image
        self.scroll = scrollbar
        self.pack(side="top", fill="both", expand=True)
        self.bind("<ButtonPress-1>", self.on_button_press)
        self.bind("<B1-Motion>", self.on_move_press)
        self.bind("<ButtonRelease-1>", self.on_button_release)

        self.rect = None

        self.start_x = None
        self.start_y = None

        self._draw_image()

    def _draw_image(self):
        self.img_tk = ImageTk.PhotoImage(image=self.image)
        self.create_image(0, 0, anchor="nw", image=self.img_tk)

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y + self.scroll.get()[0] * self.image.height

        self.rect = self.create_rectangle(self.x, self.y, 1, 1, fill="black", outline="red")

    def on_move_press(self, event):
        curX, curY = (event.x, event.y + self.scroll.get()[0] * self.image.height)

        self.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):

        pass


window = Tk()
window.title("Template maker")

a0 = Frame(window)
a1 = Button(a0, text="파일 불러오기")
a2 = Label(a0, text="파일 위치", width=70)
a3 = Button(a0, text="실행 취소")
a4 = Button(a0, text="다시 실행")
a5 = Button(a0, text="확대")
a6 = Button(a0, text="축소")
a1.grid(row=0, column=0)
a2.grid(row=0, column=1)
a3.grid(row=0, column=2)
a4.grid(row=0, column=3)
a5.grid(row=0, column=4)
a6.grid(row=0, column=5)
a0.pack(side=TOP, fill='y')

b0 = Frame(window)
b1 = Scale(b0, from_=1, to=100, orient=HORIZONTAL, length=1000)
b2 = Button(b0, text="이전 페이지")
b3 = Button(b0, text="다음 페이지")
b1.grid(row=0, column=0)
b2.grid(row=0, column=1)
b3.grid(row=0, column=2)
b0.pack(side=TOP, fill='y')

src = cv2.imread('../Exports/test84.tiff')
src = imutils.resize(src, width=1000)
img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
img = Image.fromarray(img)

c0 = Frame(window, width=1400, height=800)
c0.pack(expand=True, fill=BOTH)

# 우측 조절 바
vbar = Scrollbar(c0, orient=VERTICAL)
vbar.pack(side=RIGHT, fill=Y)

# 캔버스 설정
canvas = SrcCanvas(c0, img, vbar)
vbar.config(command=canvas.yview)

# 좌측 캔버스
canvas.config(yscrollcommand=vbar.set)
canvas.pack(side=LEFT, expand=True, fill=BOTH)


window.mainloop()

