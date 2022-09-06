import json
import os

from Refractor1.classes.book import Book
from Refractor1.classes.coord import Coord


class DataHandler:
    def __init__(self, template_name):
        self.templateName = template_name
        self.stack = []
        self.redoStack = []

    def openData(self):
        # TODO: get Data
        pass

    def appendCoordData(self, start: Coord, end: Coord):
        raw = ((start.x, start.y), (end.x, end.y), (start.w, start.h))
        self.stack.append(raw)
        self.redoStack = []

    def saveData(self):
        # TODO: save Data
        pass

    def undo(self) -> bool:
        if len(self.stack) == 0:
            return False
        self.redoStack.append(self.stack.pop())
        return True

    def redo(self) -> bool:
        if len(self.redoStack) == 0:
            return False
        self.stack.append(self.redoStack.pop())
        return True


class DataFileHandler:
    def __init__(self):
        self.filepath = "../Data/templates.json"
        self.datafile = {}

    def placeDatafile(self):
        if os.path.exists(self.filepath):
            self.datafile = self._loadDatafile()
        else:
            self.datafile = self._initDatafile()
        return self.datafile

    def saveData(self, book: Book, currentPage):
        self._structDatafile(book, currentPage)
        self._dumpDatafile()
        self.__init__()

    def deleteTemplateData(self):
        self.placeDatafile()
        self.datafile = {}
        self._dumpDatafile()

    def _initDatafile(self):
        json.dump({}, open(self.filepath, "w"), indent=2)
        with open(self.filepath, "r") as f:
            d = f.read()
        return json.loads(d)

    def _loadDatafile(self):
        with open(self.filepath, "r") as f:
            d = f.read()
            if d == "":
                return self._initDatafile()
            return json.loads(d)

    def _dumpDatafile(self):
        with open(self.filepath, "w") as f:
            json.dump(self.datafile, f, indent=2)

    def _structDatafile(self, book: Book, currentPage):
        # 파일이 가져와지지 않은 경우
        if self.datafile is None:
            self.placeDatafile()
        # 템플릿이 존재하지 않는 경우
        if not self.datafile.get(book.templateName):
            self.datafile[book.templateName] = {}
        # 파일명이 존재하지 않는 경우
        if book.title not in self.datafile[book.templateName]:
            self.datafile[book.templateName][book.title] = {}
        # 페이지 번호가 존재하지 않는 경우
        if str(currentPage) not in self.datafile[book.templateName][book.title]:
            self.datafile[book.templateName][book.title][str(currentPage)] = []
