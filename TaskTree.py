# TaskNode --> TaskTree
# TaskTree QTreeWidgetItem

from typing import List, Tuple
from PySide2 import QtCore,QtGui
from PySide2.QtWidgets import QTreeWidgetItem, QTreeWidgetItem, QWidget

from PySide2.QtGui import QColor


class TaskTreeNode(QTreeWidgetItem):
    #colors = [QColor(182,194,154),  QColor(244,208,0), QColor(138,151,123), QColor(229,131,8)]    
    colors = [QColor(182,194,184),  QColor(220,220,210)]    
    def __init__(self, parent: QWidget, desc = '', date = '', state = QtCore.Qt.CheckState.Unchecked) -> None:
        super().__init__(parent)

        if isinstance(desc, List or Tuple):
            date = desc[1]
            state = desc[2]
            desc = desc[0]

        self.setData(0, QtCore.Qt.EditRole, desc)
        self.setData(1, QtCore.Qt.EditRole, date)
        self.setData(2, QtCore.Qt.EditRole, state)
        


        self.setExpanded(False)

        self.colorIdx = 0
        if isinstance(parent, TaskTreeNode):
            self.colorIdx = (parent.colorIdx + 1) % len(TaskTreeNode.colors)

        self.setBackgroundColor(0, TaskTreeNode.colors[self.colorIdx])
        self.setBackgroundColor(1, TaskTreeNode.colors[self.colorIdx])
        self.setBackgroundColor(2, TaskTreeNode.colors[self.colorIdx])


    def isEmpty(self):
        isEmpty = True
        #检查desciption是否为空
        if self.data(0, QtCore.Qt.EditRole):
            print(self.data(0,QtCore.Qt.EditRole))
            isEmpty = False
        return isEmpty




    # def data(self, column: int, role: int):
    #     return self._data[column]

    
