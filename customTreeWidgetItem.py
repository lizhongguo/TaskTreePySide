# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'treeItemWidget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QPlainTextEdit,QDateTimeEdit


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form") 
        Form.resize(363, 178)
        self.plainTextEdit = QPlainTextEdit(Form)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setGeometry(QRect(40, 20, 191, 21))
        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(8)
        self.plainTextEdit.setFont(font)
        self.dateTimeEdit = QDateTimeEdit(Form)
        self.dateTimeEdit.setObjectName(u"dateTimeEdit")
        self.dateTimeEdit.setGeometry(QRect(40, 80, 194, 22))
        self.dateTimeEdit.setFont(font)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
    # retranslateUi

