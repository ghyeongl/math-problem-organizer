import os.path
import threading

import PyPDF2
from pdf2image import convert_from_path


class PdfConverter:
    def __init__(self):
        self.filePath = None
        self.threadList = []

        self.runAmount = 50
        self.threadAmount = 8

    # set fileH path
    def setFilePath(self, filePath):
        self.filePath = filePath

    def initConvert(self, imgInfo: tuple, startP=1, endP=None):
        if self.filePath is None or self.filePath == "":
            return False
        startP -= 1
        if endP is None:
            endP = self.getPageAmount()
        if endP > self.getPageAmount():
            raise Exception
        for i in range(startP, endP, self.runAmount):
            start = i + 1
            end = i + self.runAmount if i + self.runAmount < endP else endP
            pageRange = (start, end)
            ct = ConverterThread(self.filePath, pageRange, imgInfo)
            self.threadList.append(ct)
            print(f"Convert thread {start} to {end} created")

    def startConvert(self):
        if not self.threadList:
            return False
        print("convert started")
        workingThread = []
        for thread in self.threadList:
            thread.start()
            workingThread.append(thread)
            if len(workingThread) == self.threadAmount:
                for t in workingThread:
                    t.join()
                workingThread = []
        for t in workingThread:
            t.join()
        print("convert ended")
        self.threadList = []
        return True

    def getPageAmount(self) -> int:
        if self.filePath is None or self.filePath == "":
            return 0
        file = open(self.filePath, "rb")
        readPdf = PyPDF2.PdfFileReader(file)
        totalPages = readPdf.getNumPages()
        return totalPages


class ConverterThread(threading.Thread):
    def __init__(self, filePath, pageRange, imgInfo: tuple):
        super().__init__()
        self.filePath = filePath
        self.pageRange = pageRange
        self.imgInfo = imgInfo
        self.imgDir = imgInfo[0]
        self.fileName = imgInfo[1]
        self.imgExt = imgInfo[2]
        self.imgForm = imgInfo[3]
        self.dpi = imgInfo[4]

    def run(self):
        self._convertPdfToImage()

    def _convertPdfToImage(self):
        pages = convert_from_path(self.filePath, first_page=self.pageRange[0], last_page=self.pageRange[1], dpi=self.dpi)
        if not os.path.exists(f"{self.imgDir}/{self.fileName}"):
            os.mkdir(f"{self.imgDir}/{self.fileName}")
        for i, page in enumerate(pages):
            imgName = f"{self.imgDir}/{self.fileName}/{str(self.pageRange[0] + i)}.{self.imgExt}"
            page.save(imgName, self.imgForm)
