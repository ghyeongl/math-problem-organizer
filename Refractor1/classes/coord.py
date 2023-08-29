class Coord:
    def __init__(self, x=None, y=None, w=None, h=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def setSize(self, w, h):
        self.w = w
        self.h = h

    def setCoord(self, x, y):
        self.x = x
        self.y = y

    def setWidth(self, w):
        self.w = w

    def setHeight(self, h):
        self.h = h

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y
