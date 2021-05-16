# This Python file uses the following encoding: utf-8
from TaskTreeWidget import TaskTreeWidget
import sys
import os
from PySide2.QtGui import QBrush

from PySide2.QtWidgets import QApplication, QDateTimeEdit, QLineEdit, QMainWindow, QStyledItemDelegate, QTreeView, QTreeWidgetItem, QWidget, QWidgetItem, QVBoxLayout
from PySide2.QtCore import QFile, QSettings, Qt, QModelIndex
from PySide2.QtUiTools import QUiLoader
from TaskTree import TaskTreeNode
import PySide2
from PySide2 import QtCore, QtWidgets

import json

class TaskTreeGui(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.settings = QSettings('TaskTreeGui','UI')
        self.loadSettings()

    def closeEvent(self, event: PySide2.QtGui.QCloseEvent) -> None:
        self.settings.setValue('size', self.size())
        self.settings.setValue('pos',self.pos())
        self.settings.setValue('ttw_cw0', self.treeWidget.columnWidth(0))
        self.settings.setValue('ttw_cw1', self.treeWidget.columnWidth(1))
        print(self.treeWidget.saveData())
        json.dump(self.treeWidget.saveData(), open('data.json','w'))
        return super().closeEvent(event)

    def loadSettings(self):
        try:
            self.resize(self.settings.value('size'))
            self.move(self.settings.value('pos'))
            self.treeWidget.setColumnWidth(0, self.settings.value('ttw_cw0'))
            self.treeWidget.setColumnWidth(1, self.settings.value('ttw_cw1'))
        except:
            pass

        try:
            data = json.load(open('data.json'))
            self.treeWidget.blockSignals(True)
            self.treeWidget.loadData(data, None);
            self.treeWidget.blockSignals(False)
        except Exception as e:
            print(e)
            self.treeWidget.loadData(None, None)

    def setupUi(self, TaskTreeGui:QMainWindow):
        TaskTreeGui.setObjectName("TaskTreeGui")
        TaskTreeGui.resize(574, 474)
        self.centralwidget = QtWidgets.QWidget(parent=TaskTreeGui)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.treeWidget = TaskTreeWidget(TaskTreeGui)
        self.treeWidget.setObjectName("treeWidget")

        self.verticalLayout.addWidget(self.treeWidget)
        TaskTreeGui.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(TaskTreeGui)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 574, 22))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        TaskTreeGui.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(TaskTreeGui)
        self.statusbar.setObjectName("statusbar")
        TaskTreeGui.setStatusBar(self.statusbar)
        self.actionSave = QtWidgets.QAction(TaskTreeGui)
        self.actionSave.setObjectName("actionSave")
        self.actionLoad = QtWidgets.QAction(TaskTreeGui)
        self.actionLoad.setObjectName("actionLoad")
        self.actionExit = QtWidgets.QAction(TaskTreeGui)
        self.actionExit.setObjectName("actionExit")
        self.menuMenu.addAction(self.actionSave)
        self.menuMenu.addAction(self.actionLoad)
        self.menuMenu.addAction(self.actionExit)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(TaskTreeGui)
        QtCore.QMetaObject.connectSlotsByName(TaskTreeGui)

    def retranslateUi(self, TaskTreeGui):
        _translate = QtCore.QCoreApplication.translate
        TaskTreeGui.setWindowTitle(_translate("TaskTreeGui", "TaskTreeGui"))
        self.menuMenu.setTitle(_translate("TaskTreeGui", "Menu"))
        self.actionSave.setText(_translate("TaskTreeGui", "Save"))
        self.actionLoad.setText(_translate("TaskTreeGui", "Load"))
        self.actionExit.setText(_translate("TaskTreeGui", "Exit"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = TaskTreeGui()
    widget.show()
    sys.exit(app.exec_())
