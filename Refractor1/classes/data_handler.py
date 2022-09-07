import json
import os

from Refractor1.classes.book import Book
from Refractor1.classes.coord import Coord


class DataHandler:
    def __init__(self, template_name):
        self.templateName = template_name
        self.dataFileHandler = DataFileHandler(self)
        self.stack = []
        self.redoStack = []

    def openData(self):
        self.dataFileHandler.placeDatafile()
        pass

    def appendCoordData(self, start: Coord, end: Coord):
        raw = ((start.x, start.y), (end.x, end.y), (start.w, start.h))
        self.stack.append(raw)
        self.redoStack = []

    def saveData(self, book, page):
        self.dataFileHandler.saveData(book, page)

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

    def clear(self):
        self.stack = []
        self.redoStack = []


class DataFileHandler:
    def __init__(self, dataHandler):
        self.dataHandler = dataHandler
        self.data = None
        self.filepath = "../Data/templates.json"

    def placeDatafile(self):
        if self._loadDatafile() is None:
            self._initDatafile()
            self._loadDatafile()

    def saveData(self, book: Book, currentPage):
        if self.data is None:
            return False
        self._structDatafile(book, currentPage)
        self._appendDatafile(book, currentPage)
        return True

    def deleteTemplateData(self):
        self.placeDatafile()
        self._structDatafile(None, None)
        self.data[self.dataHandler.templateName] = {}
        self._dumpDatafile()
        self.dataHandler.clear()

    # 데이터를 파일에 쓰기
    def _appendDatafile(self, book: Book, currentPage):
        self.data[self.dataHandler.templateName][book.title][str(currentPage)] = self.dataHandler.stack
        self._dumpDatafile()
        self.dataHandler.clear()

    # 파일이 존재하는 경우 읽어오기
    def _loadDatafile(self):
        if not os.path.exists(self.filepath):
            return None
        with open(self.filepath, "r") as f:
            d = f.read()
            if d == "":
                return None
            self.data = json.loads(d)
        return self.data

    # 파일이 존재하지 않는 경우 새로 만들기
    def _initDatafile(self):
        json.dump({}, open(self.filepath, "w"), indent=2)

    # 불러온 데이터를 지우기
    def _unloadDatafile(self):
        self.data = None

    # self.data 를 파일에 쓰기
    def _dumpDatafile(self):
        with open(self.filepath, "w") as f:
            json.dump(self.data, f, indent=2)

    # 형식에 맞게 데이터를 구조화
    def _structDatafile(self, book, currentPage):
        # 파일이 가져와지지 않은 경우
        if self.data is None:
            self.placeDatafile()
        # 템플릿이 존재하지 않는 경우
        if not self.data.get(self.dataHandler.templateName):
            self.data[self.dataHandler.templateName] = {}
        if book and currentPage is not None:
            # 파일명이 존재하지 않는 경우
            if book.title not in self.data[self.dataHandler.templateName]:
                self.data[self.dataHandler.templateName][book.title] = {}
            # 페이지 번호가 존재하지 않는 경우
            if str(currentPage) not in self.data[self.dataHandler.templateName][book.title]:
                self.data[self.dataHandler.templateName][book.title][str(currentPage)] = []
