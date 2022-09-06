from PIL import Image, ImageDraw

from Refractor1.classes.coord import Coord


class ImagePainter:
    def __init__(self):
        self.path = ""
        self.image = None
        self.draw = None

        self.stack = []
        self.redoStack = []

    def loadImage(self, path):
        self.path = path
        self.stack = []
        self.redoStack = []
        self.image = Image.open(path)
        self.draw = ImageDraw.Draw(self.image)

    def reloadImage(self):
        self.draw = ImageDraw.Draw(self.image)

    def saveImage(self, extension):
        if self.image is None:
            return False
        self.image.save(self.path, extension)
        return True

    def resize(self, r_width):
        if r_width <= 0:
            return False
        if r_width == self.getWidth():
            return True
        r_height = int(r_width * (self.getHeight() / self.getWidth()))
        self.image = self.image.resize((r_width, r_height), Image.ANTIALIAS)
        self.reloadImage()
        return True

    def drawRectangle(self, start: Coord, end: Coord):
        self.stack.append(self.image.copy())
        self.redoStack = []
        self.draw.rectangle((start.x, start.y, end.x, end.y), outline=(0, 255, 0), width=3)
        self.reloadImage()

    # pageH 의 stack 에 포함되는 액션이 모두 dataH written 됨을 보장해야 함
    def undo(self) -> bool:
        if len(self.stack) == 0:
            return False
        self.redoStack.append(self.image.copy())
        self.image = self.stack.pop()
        return True

    def redo(self) -> bool:
        if len(self.redoStack) == 0:
            return False
        self.stack.append(self.image.copy())
        self.image = self.redoStack.pop()
        return True

    def getWidth(self):
        if self.image is None:
            return 0
        return self.image.size[0]

    def getHeight(self):
        if self.image is None:
            return 0
        return self.image.size[1]
