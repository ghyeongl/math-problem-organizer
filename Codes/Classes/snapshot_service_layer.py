import json
import os

from Classes import DataAccessLayer


class SnapshotServiceLayer:
    def __init__(self):
        self.accessLayer = DataAccessLayer("../../Data/snapshots.json")

    def getSnapshotsList(self):
        return self.accessLayer.snapshots
    
    def getSnapshot(self, snapshotName):
        return self.accessLayer.getSnapshot(snapshotName)
    
    def addSnapshot(self, snapshot):
        self.accessLayer.addSnapshot(snapshot)

    def removeSnapshot(self, snapshotName):
        self.accessLayer.removeSnapshot(snapshotName)
    
