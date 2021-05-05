import json
from TaskTree import *

class TaskTreeController(object):
    def __init__(self, parent:QWidget) -> None:
        super().__init__()
        self._data: dict = {}
        self._treeRoot: list = []
        self.display: list = ['isDel','description','endDate']
        self.parent = parent

    def loadJson(self, jsonStr):
        self._data = json.loads(jsonStr)
        self.parseData(self._data, self.parent)

    def parseData(self, dataList:list, parent:QWidget):
        for eachData in dataList:
            itemData = [eachData[dis] for dis in self.display]
            node = TaskTreeNode(parent, itemData)
            self.parseData(eachData['childs'], node)

    def getTreeRoot(self):
        return self._treeRoot