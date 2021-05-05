# This Python file uses the following encoding: utf-8
from TaskTreeWidget import TaskTreeWidget
import sys
import os
from PySide2.QtGui import QBrush

from PySide2.QtWidgets import QApplication, QDateTimeEdit, QLineEdit, QMainWindow, QStyledItemDelegate, QTreeView, QTreeWidgetItem, QWidget, QWidgetItem, QVBoxLayout
from PySide2.QtCore import QFile, QSettings, Qt, QModelIndex
from PySide2.QtUiTools import QUiLoader
from MainUi import Ui_TaskTreeMain
from TaskTree import TaskTreeNode
import PySide2
from PySide2 import QtCore, QtWidgets

class TaskTreeMain(Ui_TaskTreeMain,QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        #设置列数
        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)


        self.treeWidget = TaskTreeWidget(self.widget)

        #self.lineEdit = QLineEdit(self.widget)

        self.layout.addWidget(self.treeWidget)
        #self.layout.addWidget(self.lineEdit)

        self.setCentralWidget(self.widget)

        self.settings = QSettings('TaskTreeGui','UI')
        self.loadSettings()

    def closeEvent(self, event: PySide2.QtGui.QCloseEvent) -> None:
        self.settings.setValue('size', self.size())
        self.settings.setValue('pos',self.pos())
        self.settings.setValue('ttw_cw0', self.treeWidget.columnWidth(0))
        self.settings.setValue('ttw_cw1', self.treeWidget.columnWidth(1))
        print(self.treeWidget.saveData())
        return super().closeEvent(event)

    def loadSettings(self):
        try:
            self.resize(self.settings.value('size'))
            self.move(self.settings.value('pos'))
            self.treeWidget.setColumnWidth(0, self.settings.value('ttw_cw0'))
            self.treeWidget.setColumnWidth(1, self.settings.value('ttw_cw1'))
        except:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = TaskTreeMain()
    widget.show()
    sys.exit(app.exec_())
