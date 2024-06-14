


class CurrentSettings:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._snapshotName = None
        self._templateName = None
        self._studentName = None
        self._bookPath = None

    @property
    def snapshotName(self):
        return self._snapshotName

    @snapshotName.setter
    def snapshotName(self, value):
        self._snapshotName = value

    @property
    def templateName(self):
        return self._templateName

    @templateName.setter
    def templateName(self, value):
        self._templateName = value

    @property
    def studentName(self):
        return self._studentName

    @studentName.setter
    def studentName(self, value):
        self._studentName = value

    @property
    def bookPath(self):
        return self._bookPath

    @bookPath.setter
    def bookPath(self, value):
        self._bookPath = value