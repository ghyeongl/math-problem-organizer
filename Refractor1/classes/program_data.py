import json
import os


class ProgramData:
    def __init__(self):
        self.dataFileH = ProgramDataFileHandler()

    def getSnapshotsList(self):
        return self.dataFileH.snapshotsList

    def getStudentsList(self):
        return self.dataFileH.studentsList

    def addStudentsList(self, name):
        self.dataFileH.studentsList.append(name)

    def getTemplatesList(self):
        return self.dataFileH.templatesList

    def getIncorrectList(self):
        return self.dataFileH.incorrect


class ProgramDataFileHandler:
    def __init__(self):
        self.filePath = "../../Data/program_data.json"
        self.jsonM = self.JsonModifier(self.filePath)
        self.snapshotsList = ["기본 스냅샷"]
        self.studentsList = []
        self.templatesList = []
        self.incorrect = []

    def loadProgramData(self):
        self.jsonM.setupDatafile()
        self.jsonM.loadDatafile()
        return self.jsonM.getData()

    def loadSnapshotsList(self):
        self.snapshotsList = self.jsonM.getSnapshots()

    def loadStudentsList(self, snapshot):
        self.studentsList = self.jsonM.getStudents(snapshot)

    def loadTemplatesList(self, snapshot):
        self.templatesList = self.jsonM.getTemplates(snapshot)

    def loadIncorrect(self, snapshot, student, template):
        self.incorrect = self.jsonM.getIncorrect(snapshot, student, template)

    def saveProgramData(self):
        for sn in self.snapshotsList:
            self.jsonM.structSnapshotSection(sn)
            for st in self.studentsList:
                self.jsonM.structStudentSection(sn, st)

            for te in self.templatesList:
                self.jsonM.setTemplateSection(sn, te)

    class JsonModifier:
        def __init__(self, filePath):
            self.filepath = filePath
            self.data = None
            self.snapHdr = "snapshots"
            self.stuHdr = "students"
            self.tmplHdr = "templates"
            self.incrHdr = "incorrect"

        def getData(self):
            return self.data

        def setData(self, data):
            self.data = data

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

        def getSnapshots(self):
            self._structDatafile()
            return self.data[self.snapHdr].keys()

        def getStudents(self, snapshot):
            self.structSnapshotSection(snapshot)
            return self.data[self.snapHdr][snapshot][self.stuHdr].keys()

        def getStudentsDetails(self, snapshot):
            self.structSnapshotSection(snapshot)
            return self.data[self.snapHdr][snapshot][self.stuHdr]

        def getTemplates(self, snapshot):
            self.structSnapshotSection(snapshot)
            # 말단 자료형은 리스트
            return self.data[self.snapHdr][snapshot][self.tmplHdr]

        def getIncorrect(self, snapshot, student, template):
            self.structIncorrectSection(snapshot, student, template)
            # 말단 자료형은 리스트
            return self.data[self.snapHdr][snapshot][self.stuHdr][student][self.incrHdr][template]

        def structSnapshotSection(self, snapshot):
            self._structDatafile()
            if snapshot not in self.data[self.snapHdr]:
                self.data[self.snapHdr][snapshot] = {}
                self.data[self.snapHdr][snapshot][self.stuHdr] = {}
                self.data[self.snapHdr][snapshot][self.tmplHdr] = []

        def structStudentSection(self, snapshot, student):
            self.structSnapshotSection(snapshot)
            if student not in self.data[self.snapHdr][snapshot][self.stuHdr]:
                self.data[self.snapHdr][snapshot][self.stuHdr][student] = {}

        def setTemplateSection(self, snapshot, template):
            self.structSnapshotSection(snapshot)
            self.data[self.snapHdr][snapshot][self.tmplHdr] = template

        def structIncorrectSection(self, snapshot, student, template):
            self.structStudentSection(snapshot, student)
            if self.incrHdr not in self.data[self.snapHdr][self.stuHdr][student]:
                self.data[self.snapHdr][self.stuHdr][student][self.incrHdr] = {}
                self.data[self.snapHdr][self.stuHdr][student][self.incrHdr][template] = []

        def setIncorrectSection(self, snapshot, student, template, incorrect):
            self.structIncorrectSection(snapshot, student, template)
            for i in incorrect:
                self.data[self.snapHdr][self.stuHdr][student][self.incrHdr][template].append(i)

        def getIncorrectSection(self, snapshot, student, template):
            self.structIncorrectSection(snapshot, student, template)
            return self.data[self.snapHdr][self.stuHdr][student][self.incrHdr][template]

        def _loadDatafile(self):
            if not os.path.exists(self.filepath):
                return None
            with open(self.filepath, "r") as f:
                d = f.read()
                if d == "":
                    return None
            return json.loads(d)

        def _unloadDatafile(self):
            self.data = None

        def _initDatafile(self):
            json.dump({}, open(self.filepath, "w"), indent=2)

        def _dumpDatafile(self):
            with open(self.filepath, "w") as f:
                json.dump(self.data, f, indent=2)

        def _structDatafile(self):
            if self.data is None:
                self.loadDatafile()
            if not self.data.get(self.snapHdr):
                self.data[self.snapHdr] = {}


