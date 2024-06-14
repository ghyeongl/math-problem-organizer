import os.path

from Refractor1.classes.data_handler import DataHandler
from Refractor1.classes.file_handler import FileHandler
from Refractor1.classes.image_painter import ImagePainter
from Codes.Classes import DataAccessLayer
from Codes.Classes import Snapshot


class TemplateServiceLayer:
    def __init__(self):
        self.currentSnapshot = None
        pass
    
    def setSnapshot(self, snapshot):
        self.currentSnapshot:Snapshot = snapshot
    
    def getTemplatesList(self):
        if self.currentSnapshot is None:
            Exception('Snapshot not set')
        return self.currentSnapshot.templates
    
    def getTemplate(self, name):
        if self.currentSnapshot is None:
            Exception('Snapshot not set')
        return self.currentSnapshot.getTemplate(name)

    def addTemplate(self, template):
        if self.currentSnapshot is None:
            Exception('Snapshot not set')
        self.currentSnapshot.addTemplate(template)
    
    def removeTemplate(self, name):
        if self.currentSnapshot is None:
            Exception('Snapshot not set')
        self.currentSnapshot.removeTemplate(name)
    

class TemplateModifier:
    def __init__(self):
        self.accessLayer = DataAccessLayer("../../Data/program_data.json")
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
        self.dataHandler.saveData(self.fileHandler.getFile(), self.currentPage)
        return True

    def saveImageOnly(self):
        if self.imagePainter.image is None:
            return False
        if os.path.exists(self.imagePainter.path):
            self.imagePainter.saveImage(self.fileHandler.imgForm)
            return True
        return False
