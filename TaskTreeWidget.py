# This Python file uses the following encoding: utf-8
from ItemWidget import ItemWidget
import sys
import os
from PySide2.QtGui import QBrush, QPainter, QPen

from PySide2.QtWidgets import QApplication, QCheckBox, QDateTimeEdit, QDialogButtonBox, QHBoxLayout, QMainWindow, QMenu, QPlainTextEdit, QPushButton, QStyle, QStyledItemDelegate, QTextEdit, QTreeView, QTreeWidget, QTreeWidgetItem, QWidget, QWidgetItem,QLineEdit
from PySide2.QtCore import QFile, QMargins, Qt, QModelIndex
from PySide2.QtUiTools import QUiLoader
from MainUi import Ui_TaskTreeMain
from TaskTree import TaskTreeNode
import PySide2
from PySide2 import QtCore, QtWidgets,QtGui

class Header(QtWidgets.QHeaderView):
    def __init__(self, orientation, parent=None):
        super(Header, self).__init__(orientation, parent)

        self.button = QTextEdit('',self)
        self.button.setContentsMargins(0,0,0,0)


class ButtonBox(QWidget):
    def __init__(self, parent, node) -> None:
        super().__init__(parent=parent)
        self.layout = QHBoxLayout(self)
        self.buttonPlus = QPushButton('+', self)
        self.buttonPlus.setContentsMargins(0,0,0,0)
        self.buttonMinus = QPushButton('-', self)
        self.buttonMinus.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.buttonPlus)
        self.layout.addWidget(self.buttonMinus)
        self.setContentsMargins(0,0,0,0)
        self.node = node
        self.par = parent

        self.buttonPlus.clicked.connect(self.onPlus)
        self.buttonMinus.clicked.connect(self.onMinus)

    def onPlus(self):
        self.par.createTaskTreeNode(self.node)

    def onMinus(self):
        self.par.removeTaskTreeNode(self.node)
        

class TaskTreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


        self.setColumnCount(4)

        #设置树形控件头部的标题
        self.setHeaderLabels(['description','deadline','state', 'action'])
        self.setRootIsDecorated(True)
        #设置树形控件的列的宽度
        # self.setHeaderHidden(True)

        # self.createHeader()

        # self.setColumnWidth(0,400)

        #设置根节点
        # root = TaskTreeNode(self, ['Root'])

        #root=QTreeWidgetItem(self.treeWidget)
        # root.setText(0,'Root')
        # root.setIcon(0,QIcon('./images/root.png'))

        # todo 优化2 设置根节点的背景颜色
        # brush_red=QBrush(Qt.red)
        # root.setBackground(0,brush_red)
        # brush_blue=QBrush(Qt.blue)
        # root.setBackground(1,brush_blue)

        #设置子节点1
        # child1=QTreeWidgetItem()
        # child1.setText(0,'child1')
        # child1.setText(1,'ios')
        # child1.setIcon(0,QIcon('./images/IOS.png'))
        # child1 = TaskTreeNode(root, ['child', '2021-03-04'])

        # root2 = TaskTreeNode(self, ['Root2'])
        # child12 = TaskTreeNode(root2, ['1','2028-03-01'])

        #自定义显示
        # self.setItemWidget(root,0,ItemWidget(root,self))

        #todo 优化1 设置节点的状态
        # child1.setCheckState(0,Qt.Checked)
        # child1.setText(0,'child1')
        # child1.setText(1,'ios')
        # root.addChild(child1)

        #加载根节点的所有属性与子控件
        # self.addTopLevelItem(root)

        #响应双击时间
        self.doubleClicked.connect(self.onDoubleClicked)
        # self.itemChanged.connect(self.onItemChanged)
        #self.treeWidget.clicked.connect(self.onClicked)

        #节点全部展开
        # self.expandAll()

        #双击不影响展开
        self.setExpandsOnDoubleClick(False)

        #self.setItemDelegateForColumn(1, DatetimeDelegate(self))
        self.setItemDelegate(DatetimeDelegate(self))

        # 配置treewidget策略
        # self.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.customContextMenuRequested.connect(self.onMenuRequested)

        #双击顶部显示事件
        self.header().setSectionsClickable(True)
        self.header().sectionClicked.connect(self.onSectionClicked)

        # headerItem = QTreeWidgetItem()
        # headerItem.setText(0, 'A')
        # headerItem.setText(1, 'B')
        # headerItem.setText(2, 'C')
        # headerItem.setText(3, 'D')
        # self.setItemWidget(headerItem,3,QPushButton('Add'))
        # self.setHeaderItem(headerItem)
        # self.setHeaderItem()

    def onSectionClicked(self):
        self.addTopLevelItem(self.createTaskTreeNode(self))

    def createHeader(self):
        header = Header(QtCore.Qt.Horizontal, self)
        self.setHeader(header)

    def createTaskTreeNode(self, parent, taskData=None):
        if not taskData:
            taskData = ''
        node = TaskTreeNode(parent, taskData)

        buttonBox = ButtonBox(self, node)

        self.setItemWidget(node, 3, buttonBox)
        return node

    def removeTaskTreeNode(self, node:TaskTreeNode):
        parent = node.parent()
        if parent:
            parent.takeChild(parent.indexOfChild(node))
        else:
            self.takeTopLevelItem(self.indexOfTopLevelItem(node))


    def loadData(self, data, parent):
        if data:
            for taskData in data:
                cur = None
                if parent is None:
                    cur = self.createTaskTreeNode(self, taskData['data'])
                    self.addTopLevelItem(cur)
                else:
                    cur = self.createTaskTreeNode(parent, taskData['data'])

                self.loadData(taskData['child'], cur)


    def saveData(self, item : TaskTreeNode = None, dataDict: dict = None):
        # first save item's data
        # then save its child

        if item is None:
            dataList = []
            for idx in range(self.topLevelItemCount()):
                treeNode = self.topLevelItem(idx)
                dataDict = {}
                self.saveData(treeNode, dataDict)
                dataList.append(dataDict)
            return dataList

        if not item.isEmpty():
            dataDict['data'] = [item.data(i, Qt.EditRole) for i in range(item.columnCount())]
            dataDict['child'] = []
            for i in range(item.childCount()):
                cDataDict = {}
                self.saveData(item.child(i), cDataDict)
                dataDict['child'].append(cDataDict)


    def onMenuRequested(self, pos):
        item = self.currentItem()

        popMenu = QMenu(self)
        addAct = popMenu.addAction("&Add")
        delAct = popMenu.addAction("&Delete")
        action = popMenu.exec_(self.mapToGlobal(pos))

        if action == addAct:
            #添加操作                
            task = TaskTreeNode(item if item is not None else self, ['Test',''])
        elif action == delAct:
            if item.parent() == None:
                self.takeTopLevelItem(self.indexOfTopLevelItem(item))
            else:
                parentItem = item.parent()
                parentItem.takeChild(parentItem.indexOfChild(item))

    # def onClicked(self,qmodeLindex:QModelIndex):
    #     item=self.treeWidget.currentItem()
    #     item.setFlags(item.flags()|Qt.ItemIsEditable)

    def onDoubleClicked(self,qmodeLindex:QModelIndex):
        item=self.currentItem()
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.editItem(item, qmodeLindex.column())

class DatetimeDelegate(QStyledItemDelegate):
    def __init__(self, parent) -> None:
        super().__init__(parent=parent)

    def createEditor(self, parent: PySide2.QtWidgets.QWidget, option: PySide2.QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex) -> QtWidgets.QWidget:
        if index.column() == 1:
            datetimeEdit = QDateTimeEdit(parent)
            datetimeEdit.setCalendarPopup(True)
            datetimeEdit.activateWindow()
            return datetimeEdit
    
        if index.column() == 2:
            chkBox = QCheckBox('Finished', parent)
            if index.model().data(index, Qt.EditRole) == 'Unfinished':
                chkBox.setChecked(False)
            else:
                chkBox.setChecked(True)
            return chkBox

        #return ItemWidget(parent)

        #return super().createEditor(parent, option, index)

        return QLineEdit(parent)

    def setModelData(self, editor: PySide2.QtWidgets.QWidget, model: QtCore.QAbstractItemModel, index: QtCore.QModelIndex) -> None:
        if index.column()==2:
            cb:QCheckBox = editor
            if cb.checkState() == Qt.CheckState.Checked:
                model.setData(index, 'Finished', Qt.EditRole)
            else:
                model.setData(index, 'Uninished', Qt.EditRole)
            return
        model.setData(index, editor.text())
        return

    # 通过重载下面两个函数，可实现自定义样式的绘制
    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex) -> None:

        super().paint(painter, option, index)
        checked = index.model().data(index.model().index(index.row(),2,index.parent()))
        # print(checked,index.row(),index.column())        
        if checked == 'Finished':
            pen = QPen(Qt.black, 2, Qt.SolidLine)
            painter.setPen(pen)
            rect:QtCore.QRect = option.rect

            y = int(0.5*rect.height() + rect.y())
            painter.drawLine(rect.x(),y,rect.x()+rect.width(),y)



    def editorEvent(self, event: PySide2.QtCore.QEvent, model: PySide2.QtCore.QAbstractItemModel, option: PySide2.QtWidgets.QStyleOptionViewItem, index: PySide2.QtCore.QModelIndex) -> bool:
        return super().editorEvent(event, model, option, index)
