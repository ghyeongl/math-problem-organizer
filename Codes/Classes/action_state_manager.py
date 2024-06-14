import json
import os

from Codes.Classes.data_access_layer import Coord
from Codes.Classes.template_service_layer import TemplateServiceLayer



class ActionStateManager:
    # template 이름을 받음 / datafilehandler에서 템플릿 이름을 가져와서 json을 읽음
    def __init__(self, templateService: TemplateServiceLayer):
        # self.dataFileHandler = DataFileHandler(self)
        self.templateService = templateService
        self.stack = []
        self.redoStack = []

    def appendCoordData(self, start: Coord, end: Coord):
        raw = ((start.x, start.y), (end.x, end.y), (start.w, start.h))
        self.stack.append(raw)
        self.redoStack = []

    def saveData(self, file, page):
        self.dataFileHandler.saveData(file, page)
        self.templateService.saveData()

    def undo(self) -> bool:
        if len(self.stack) == 0:
            print("nothing to undo")
            return False
        self.redoStack.append(self.stack.pop())
        return True

    def redo(self) -> bool:
        if len(self.redoStack) == 0:
            print("nothing to redo")
            return False
        self.stack.append(self.redoStack.pop())
        return True



'''
class DataFileHandler:
    def __init__(self, dataHandler):
        self.dataHandler = dataHandler
        self.data = None
        self.filepath = "../../Data/templates.json"

    def placeDatafile(self):
        if self._loadDatafile() is None:
            print("loadDatafile returned None")
            self._initDatafile()
            self._loadDatafile()

    def getData(self):
        return self.data

    def getCoords(self, template, file, page):
        self.placeDatafile()
        if not self.data[template].get(file):
            return False
        if not self.data[template][file].get(str(page)):
            return False
        return self.data[template][file][str(page)]

    def saveData(self, file, currentPage):
        self._structDatafile(file, currentPage)
        self._appendDatafile(file, currentPage)
        return True

    def deleteTemplateData(self):
        self.placeDatafile()
        self._structDatafile(None, None)
        self.data[self.dataHandler.templateName] = {}
        self._dumpDatafile()
        self.dataHandler.clear()

    # 데이터를 파일에 쓰기
    def _appendDatafile(self, file, currentPage):
        for i in self.dataHandler.stack:
            self.data[self.dataHandler.templateName][file][str(currentPage)].append(i)
        self._dumpDatafile()
        self.dataHandler.clear()

    # 파일이 존재하는 경우 읽어오기
    def _loadDatafile(self):
        if not os.path.exists(self.filepath):
            print("File not found")
            return None
        with open(self.filepath, "r", encoding="UTF-8") as f:
            d = f.read()
            if d == "":
                print("File is empty")
                return None
            self.data = json.loads(d)
        return self.data

    # 파일이 존재하지 않는 경우 새로 만들기
    def _initDatafile(self):
        json.dump({}, open(self.filepath, "w"), indent=2, ensure_ascii=False)

    # 불러온 데이터를 지우기
    def _unloadDatafile(self):
        self.data = None

    # self.data 를 파일에 쓰기
    def _dumpDatafile(self):
        with open(self.filepath, "w") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    # 형식에 맞게 데이터를 구조화
    def _structDatafile(self, file, currentPage):
        # 파일이 가져와지지 않은 경우
        if self.data is None:
            self.placeDatafile()
        # 템플릿이 존재하지 않는 경우
        if not self.data.get(self.dataHandler.templateName):
            self.data[self.dataHandler.templateName] = {}
        if file and currentPage is not None:
            # 파일명이 존재하지 않는 경우
            if file not in self.data[self.dataHandler.templateName]:
                self.data[self.dataHandler.templateName][file] = {}
            # 페이지 번호가 존재하지 않는 경우
            if str(currentPage) not in self.data[self.dataHandler.templateName][book.title]:
                self.data[self.dataHandler.templateName][book.title][str(currentPage)] = []
'''