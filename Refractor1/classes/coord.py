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
