import os
import shutil

from Refractor1.classes.pdf_converter import PdfConverter


class FileHandler:
    def __init__(self):
        self.filePath = ""
        self.fileName = ""
        self.totalPage = 1

        self.pdfConverter = PdfConverter()

        self.fileDir = "../../Exports/Temp_Books"
        self.imgDir = "../../Exports/Temp_Images"
        self._checkTempDir()

        self.imgExt = "jpg"
        self.imgForm = "JPEG"
        self.imgDpi = 200
        self.imgInfo = None

    def checkFileImported(self):
        return self.filePath != ""

    def importFile(self, file):
        self.filePath = file
        if self.filePath == "":
            return False
        self.fileName = self.filePath.split("/")[-1]
        return True

    def initFile(self):
        if self.filePath == "":
            return False
        # cleanup before import
        shutil.rmtree(self.imgDir)
        os.mkdir(self.imgDir)
        # should copied to fileDir
        shutil.copy(self.filePath, f"{self.fileDir}/{self.fileName}")
        self.filePath = f"{self.fileDir}/{self.fileName}"
        # should convert to images and get amount of pagesH
        self.pdfConverter.setFilePath(self.filePath)
        self.totalPage = self.pdfConverter.getPageAmount()
        self.imgInfo = (self.imgDir, self.fileName, self.imgExt, self.imgForm, self.imgDpi)
        self.pdfConverter.initConvert(self.imgInfo)
        return self.pdfConverter.startConvert()

    # return image path (to be used in ImagePainter)
    # when input integer
    def getPathOfPage(self, page):
        return f"{self.imgDir}/{self.fileName}/{page}.{self.imgExt}"

    # check availability of each temp directory
    def _checkTempDir(self):
        if not os.path.exists(self.fileDir):
            os.mkdir(self.fileDir)
        if not os.path.exists(self.imgDir):
            os.mkdir(self.imgDir)
        return True
