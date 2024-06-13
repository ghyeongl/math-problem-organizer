import json


class Coord:
    def __init__(self, data={
        'bookpath': '', 
        'page': 0, 
        'xy': [None, None], 
        'wh': [None, None],
        'booksize': [None, None]
        }):
        self.bookpath = data['bookpath']
        self.page = data['page']
        self.x = data['xy'][0]
        self.y = data['xy'][1]
        self.w = data['wh'][0]
        self.h = data['wh'][1]
        self.bw = data['booksize'][0]
        self.bh = data['booksize'][1]
        
    def __init__(self, bookpath='', page='', x=None, y=None, w=None, h=None, bw=None, bh=None):
        self.bookpath = bookpath
        self.page = page
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.bw = bw
        self.bh = bh

    def setBook(self, bookpath, page):
        self.bookpath = bookpath
        self.page = page
        
    def setSize(self, w, h):
        self.w = w
        self.h = h

    def setStartPoint(self, x, y):
        self.x = x
        self.y = y
    
    def setEndPoint(self, x, y):
        self.w = (x - self.x) if self.bw is not None and x < self.bw else self.bw - self.x
        self.h = (y - self.y) if self.bh is not None and y < self.bh else self.bh - self.y
    
    def setBookSize(self, bw, bh):
        self.bw = bw
        self.bh = bh

    @property
    def data(self):
        return {
                'bookpath': self.bookpath,
                'page': self.page,
                'xy': [self.x, self.y],
                'wh': [self.w, self.h],
                'booksize': [self.bw, self.bh]
        }


class Incorrect:
    def __init__(self, data={'name': '', 'template': '', 'coord': []}):
        self.name = data['name']
        self.template = data['template']
        self.coord = Coord(data['coord'])
    
    def __init__(self, name, template, coord: Coord):
        self.name = name
        self.template = template
        self.coord = coord
    
    @property
    def data(self):
        return {
                'name': self.name,
                'template': self.template,
                'coord': self.coord.data,
        }


class Student:
    def __init__(self, data={'name': '', 'incorrects': []}):
        self.name = data['name']
        self._incorrects = [Incorrect(d) for d in data['incorrects']]
    
    @property
    def incorrects(self):
        return self._incorrects

    def addIncorrect(self, incorrect: Incorrect):
        self._incorrects.append(incorrect)

    def removeIncorrect(self, name):
        for incorrect in self._incorrects:
            if incorrect.name == name:
                self._incorrects.remove(incorrect)
                return
        Exception('Incorrect not found')

    @property
    def data(self):
        return {
                'name': self.name,
                'incorrects': [wa.data for wa in self._incorrects]
        }


class Template:
    def __init__(self, data={'name': '', 'coords': []}):
        self._name = data['name']
        self._coords:list[Coord] = [Coord(d) for d in data['coords']]
    
    @property
    def data(self):
        return {
                'name': self.name,
                'coords': [c.data for c in self.coords],
        }


class Snapshot:
    def __init__(self, data={'name': '', 'students': [], 'templates': []}):
        self._name = data['name']
        self._students = [Student(d) for d in data['students']]
        self._templates = [Template(d) for d in data['templates']]

    def __init__(self, name, students: list[Student]=[], templates: list[Template]=[]):
        self._name = name
        self._students = students
        self._templates = templates

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name: str):
        self._name = name

    
    # Students의 getter와 setter.
    # addStudent: Student 추가
    # removeStudent: Student 제거
    # getStudent: Student 반환
    @property
    def students(self):
        return self._students
    
    def getStudent(self, name):
        for student in self.students:
            if student.name == name:
                return student
        Exception('Student not found')
    
    def addStudent(self, student: Student):
        self.students.append(student)
    
    def removeStudent(self, name):
        for student in self.students:
            if student.name == name:
                self.students.remove(student)
                return
        Exception('Student not found')

    # Templates의 getter와 setter.
    # addTemplate: Template 추가
    # removeTemplate: Template 제거
    # getTemplate: Template 반환
    @property
    def templates(self):
        return self._templates
    
    def getTemplate(self, name):
        for template in self.templates:
            if template.name == name:
                return template
        Exception('Template not found')
    
    def addTemplate(self, template):
        self.templates.append(template)
    
    def removeTemplate(self, name):
        for template in self.templates:
            if template.name == name:
                self.templates.remove(template)
                return
        Exception('Template not found')

    def data(self):
        return {
                'name': self.name,
                'students': [s.data for s in self.students],
                'templates': [t.data for t in self.templates],
        }
    

class DataAccessLayer:
    def __init__(self, filepath):
        self.filepath = filepath
        self._snapshots = []
        self.loadFromFile()

    @property
    def snapshots(self):
        return self._snapshots

    def addSnapshot(self, snapshot: Snapshot):
        self._snapshots.append(snapshot)

    def getSnapshot(self, name):
        for snapshot in self._snapshots:
            if snapshot.name == name:
                return snapshot
        return None

    def saveToFile(self):
        with open(self.filepath, 'w') as f:
            json.dump([s.save() for s in self._snapshots], f)

    def loadFromFile(self):
        with open(self.filepath, 'r') as f:
            data = json.load(f)
            self._snapshots = [Snapshot(d) for d in data]
