import os.path

from Refractor1.classes.data_handler import DataHandler
from Refractor1.classes.file_handler import FileHandler
from Refractor1.classes.image_painter import ImagePainter


class Template:
    def __init__(self, template_name):
        self.templateName = template_name
        self.fileHandler = FileHandler()
        self.dataHandler = DataHandler(template_name)
        self.imagePainter = ImagePainter()

        self.currentPage = 0

    def getImagePath(self):
        return self.fileHandler.getPathOfPage(self.currentPage)

    def setFile(self, file):
        self.save()
        if self.fileHandler.importFile(file):
            return self.fileHandler.initFile()
        return False

    def setPage(self, page, resize=True):
        self.save()
        page = int(page)
        self.imagePainter.loadImage(self.fileHandler.getPathOfPage(page))
        self.currentPage = page
        if resize:
            self.imagePainter.resize(1000)
        return True

    def nextPage(self):
        if self.currentPage >= self.fileHandler.totalPage:
            return False
        return self.setPage(self.currentPage + 1)

    def prevPage(self):
        if self.currentPage < 2:
            return False
        return self.setPage(self.currentPage - 1)

    def changeImageSize(self):
        if self.imagePainter is None:
            return False
        if self.imagePainter.getWidth() == 1000:
            self.imagePainter.resize(500)
        elif self.imagePainter.getWidth() == 500:
            self.imagePainter.resize(1000)
        else:
            self.imagePainter.resize(1000)
        return True

    def addRectangle(self, start, end):
        self.imagePainter.drawRectangle(start, end)
        self.dataHandler.appendCoordData(start, end)
        return True

    def undo(self):
        if self.imagePainter is None:
            return False
        d = self.dataHandler.undo()
        i = self.imagePainter.undo()
        return d and i

    def redo(self):
        if self.imagePainter is None:
            return False
        d = self.dataHandler.redo()
        i = self.imagePainter.redo()
        return d and i

    def getWidth(self):
        return self.imagePainter.getWidth()

    def getHeight(self):
        return self.imagePainter.getHeight()

    def getTotalPage(self):
        return self.fileHandler.totalPage

    def save(self):
        self.saveImageOnly()
        self.dataHandler.saveData(self.fileHandler.getBook(), self.currentPage)
        return True

    def saveImageOnly(self):
        if self.imagePainter.image is None:
            return False
        if os.path.exists(self.imagePainter.path):
            self.imagePainter.saveImage(self.fileHandler.imgForm)
            return True
        return False
