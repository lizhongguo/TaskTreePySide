# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ItemWidget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtWidgets import QHBoxLayout,QPlainTextEdit,QPushButton,QWidget, QWidgetItem, QLineEdit


class ItemWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(ItemWidget, self).__init__(*args, **kwargs)
        #self.setGeometry(QRect(10, 10, 271, 61))
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setObjectName("lineEdit")
        #self.lineEdit.setContentsMargins(0,0,0,0)
        self.horizontalLayout.addWidget(self.lineEdit)
        self.ToolButton = QPushButton(self)
        self.ToolButton.setObjectName("ToolButton")
        self.horizontalLayout.addWidget(self.ToolButton)

    def sizeHint(self):
        return QSize(100,20)
