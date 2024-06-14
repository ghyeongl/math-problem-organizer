import json
import os


class ProgramDataFileHandler:
    def __init__(self):
        self.filePath = "../../Data/program_data.json"
        self.jsonM = self.JsonModifier(self.filePath)
        self.snapshotsList = []
        self.loadSnapshotsList()
        self.snapshot = ""
        self.studentsList = []
        self.templatesList = []
        self.incorrect = []

    # 데이터 읽기 / 쓰기
    def loadProgramData(self):
        self.jsonM.setupDatafile()
        self.jsonM.loadDatafile()
        return self.jsonM.getData()

    def saveProgramData(self, snapshot):
        self.jsonM.structSnapshotSection(snapshot)
        if self.snapshot == snapshot:
            for st in self.studentsList:
                self.jsonM.structStudentSection(snapshot, st)
            self.jsonM.setTemplatesSection(snapshot, self.templatesList)
            self.jsonM.dumpDatafile()

    # 스냅샷
    def getSnapshotsList(self):
        return self.snapshotsList

    def loadSnapshotsList(self):
        self.snapshotsList = self.jsonM.getSnapshots()

    def setCurrentSnapshot(self, snapshot):
        self.snapshot = snapshot

    def appendSnapshot(self, snapshot):
        if snapshot in self.snapshotsList:
            return False
        self.snapshotsList.append(snapshot)
        self.saveProgramData(snapshot)
        return True

    # 학생
    def getStudentsList(self):
        if self.snapshot == "":
            return None
        return self.studentsList

    def loadStudentsList(self):
        if self.snapshot == "":
            return False
        self.studentsList = self.jsonM.getStudents(self.snapshot)
        return True

    def appendStudent(self, student):
        if self.snapshot == "":
            return False
        if student in self.studentsList:
            return False
        self.studentsList.append(student)
        self.saveProgramData(self.snapshot)
        return True

    def modifyStudent(self, student, newName):
        if self.snapshot == "":
            return False
        if student not in self.studentsList:
            return False
        self.jsonM.modifyStudentSection(self.snapshot, student, newName)
        return True

    # 템플릿
    def getTemplatesList(self):
        if self.snapshot == "":
            return None
        return self.templatesList

    def loadTemplatesList(self):
        if self.snapshot == "":
            return False
        self.templatesList = self.jsonM.getTemplates(self.snapshot)
        return True

    def appendTemplate(self, template):
        if self.snapshot == "":
            return False
        self.templatesList.append(template)
        self.saveProgramData(self.snapshot)
        return True

    def modifyTemplate(self, template, newName):
        if self.snapshot == "":
            return False
        if template not in self.templatesList:
            return False
        self.jsonM.modifyTemplatesSection(self.snapshot, template, newName)

    def deleteTemplate(self, snapshot, template):
        if self.snapshot != snapshot:
            return False
        self.templatesList.remove(template)
        self.saveProgramData(self.snapshot)
        return True

    # 오답
    def getIncorrect(self, student, template):
        if self.snapshot == "":
            return None
        self.loadIncorrect(student, template)
        return self.incorrect

    def loadIncorrect(self, student, template):
        if self.snapshot == "":
            return False
        if student == "" or template == "":
            return False
        self.incorrect = self.jsonM.getIncorrect(self.snapshot, student, template)
        return True

    def saveDataWithIncorrect(self, student, template):
        if self.snapshot == "":
            return False
        self.jsonM.setIncorrectSection(self.snapshot, student, template, self.incorrect)
        self.saveProgramData(self.snapshot)
        return True

    def deleteAllIncorrect(self, student, template):
        if self.snapshot == "":
            return False
        self.jsonM.delIncorrectSection(self.snapshot, student, template)
        self.saveProgramData(self.snapshot)
        return True

    class JsonModifier:
        def __init__(self, filePath):
            self.filepath = filePath
            self.data = None
            self.snapHdr = "snapshots"
            self.stuHdr = "students"
            self.tmplHdr = "templates"
            self.incrHdr = "incorrect"

        # 데이터
        def getData(self):
            return self.data

        def setData(self, data):
            self.data = data

        # 파일 입출력
        def loadDatafile(self):
            self.data = self._loadDatafile()
            if self.data is None:
                self._initDatafile()
                self.loadDatafile()

        def setupDatafile(self):
            self._structDatafile()
            self.dumpDatafile()

        def dumpDatafile(self):
            self._dumpDatafile()

        # 스냅샷
        def getSnapshots(self):
            self._structDatafile()
            return list(self.data[self.snapHdr].keys())

        def structSnapshotSection(self, snapshot):
            if snapshot is None or snapshot == "":
                return False
            self._structDatafile()
            if snapshot not in self.data[self.snapHdr]:
                self.data[self.snapHdr][snapshot] = {}
                self.data[self.snapHdr][snapshot][self.stuHdr] = {}
                self.data[self.snapHdr][snapshot][self.tmplHdr] = []

        # 학생
        def getStudents(self, snapshot):
            self.structSnapshotSection(snapshot)
            return list(self.data[self.snapHdr][snapshot][self.stuHdr].keys())

        def getStudentDetails(self, snapshot, student):
            self.structSnapshotSection(snapshot)
            return self.data[self.snapHdr][snapshot][self.stuHdr][student]

        def structStudentSection(self, snapshot, student):
            if student is None or student == "":
                return False
            self.structSnapshotSection(snapshot)
            if student not in self.data[self.snapHdr][snapshot][self.stuHdr]:
                self.data[self.snapHdr][snapshot][self.stuHdr][student] = {}

        def modifyStudentSection(self, snapshot, student, newName):
            if newName is None or newName == "":
                return False
            studentData = self.getStudentDetails(snapshot, student)
            self.delStudentSection(snapshot, student)
            self.structStudentSection(snapshot, newName)
            self.setStudentSection(snapshot, newName, studentData)
            return True

        def setStudentSection(self, snapshot, newName, studentData):
            self.structStudentSection(snapshot, newName)
            self.data[self.snapHdr][snapshot][self.stuHdr][newName] = studentData

        def delStudentSection(self, snapshot, student):
            if student in self.data[self.snapHdr][snapshot][self.stuHdr]:
                del self.data[self.snapHdr][snapshot][self.stuHdr][student]
                return True
            return False

        # 템플릿
        def getTemplates(self, snapshot):
            self.structSnapshotSection(snapshot)
            # 말단 자료형은 리스트
            return self.data[self.snapHdr][snapshot][self.tmplHdr]

        def setTemplatesSection(self, snapshot, template):
            if template is None or template == "":
                return False
            self.structSnapshotSection(snapshot)
            self.data[self.snapHdr][snapshot][self.tmplHdr] = template

        def modifyTemplatesSection(self, snapshot, template, newName):
            if newName is None or newName == "":
                return False
            self.structSnapshotSection(snapshot)
            self.data[self.snapHdr][snapshot][self.tmplHdr].remove(template)
            self.data[self.snapHdr][snapshot][self.tmplHdr].append(newName)
            return True

        # 오답
        def getIncorrect(self, snapshot, student, template):
            self.structIncorrectSection(snapshot, student, template)
            # 말단 자료형은 리스트
            return self.data[self.snapHdr][snapshot][self.stuHdr][student][self.incrHdr][template]

        def structIncorrectSection(self, snapshot, student, template):
            self.structStudentSection(snapshot, student)
            if self.incrHdr not in self.data[self.snapHdr][snapshot][self.stuHdr][student]:
                self.data[self.snapHdr][snapshot][self.stuHdr][student][self.incrHdr] = {}
                self.data[self.snapHdr][snapshot][self.stuHdr][student][self.incrHdr][template] = []

        def setIncorrectSection(self, snapshot, student, template, incorrect: list):
            self.structIncorrectSection(snapshot, student, template)
            self.data[self.snapHdr][self.stuHdr][student][self.incrHdr][template] = incorrect

        def delIncorrectSection(self, snapshot, student, template):
            self.structIncorrectSection(snapshot, student, template)
            self.data[self.snapHdr][self.stuHdr][student][self.incrHdr][template] = []

        # Private
        def _loadDatafile(self):
            if not os.path.exists(self.filepath):
                return None
            with open(self.filepath, "r", encoding="UTF-8") as f:
                d = f.read()
                if d == "":
                    return None
            return json.loads(d)

        def _unloadDatafile(self):
            self.data = None

        def _initDatafile(self):
            json.dump({}, open(self.filepath, "w"), indent=2, ensure_ascii=False)

        def _dumpDatafile(self):
            with open(self.filepath, "w") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)

        def _structDatafile(self):
            if self.data is None:
                self.loadDatafile()
            if not self.data.get(self.snapHdr):
                self.data[self.snapHdr] = {}
