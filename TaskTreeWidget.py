# This Python file uses the following encoding: utf-8
from ItemWidget import ItemWidget
import sys
import os
from PySide2.QtGui import QBrush, QPainter, QPen

from PySide2.QtWidgets import QApplication, QDateTimeEdit, QMainWindow, QMenu, QPlainTextEdit, QStyledItemDelegate, QTreeView, QTreeWidget, QTreeWidgetItem, QWidgetItem,QLineEdit
from PySide2.QtCore import QFile, Qt, QModelIndex
from PySide2.QtUiTools import QUiLoader
from MainUi import Ui_TaskTreeMain
from TaskTree import TaskTreeNode
import PySide2
from PySide2 import QtCore, QtWidgets,QtGui

class TaskTreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setColumnCount(2)
        #设置树形控件头部的标题
        self.setHeaderLabels(['description','deadline'])
        self.setRootIsDecorated(True)
        #设置树形控件的列的宽度

        self.setColumnWidth(0,400)

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
        self.itemChanged.connect(self.onItemChanged)
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

        self.loadData()

    def loadData(self):
        self.addTopLevelItem(TaskTreeNode(self, ['','']))


    def saveData(self, item : TaskTreeNode = None, dataDict: dict = None):
        # first save item's data
        # then save its child

        if item is None:
            dataList = []
            for idx in range(self.topLevelItemCount()-1):
                treeNode = self.topLevelItem(idx)
                dataDict = {}
                self.saveData(treeNode, dataDict)
                dataList.append(dataDict)
            return dataList

        if not item.isEmpty():
            dataDict['data'] = [item.data(i, Qt.EditRole) for i in range(item.columnCount())]
            dataDict['child'] = []
            for i in range(item.childCount()-1):
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

    def onItemChanged(self, item:TaskTreeNode, column:int):
        #可以在这儿实现删除
        #保持最后一行为空

        # 1. 非空行都包含一个空子行, 默认不展开,空行不包含子行
        # 2. 如果将空行修改为了非空行,则需要增加一个空行
        # 3. 如果将非空行修改为了空行,则需要删除该行

        # 判断item是否是最后一个
        isLast = True
        parent = item.parent()
        if parent is None:
            isLast = self.indexOfTopLevelItem(item) == self.topLevelItemCount()-1
        else:
            isLast = parent.indexOfChild(item) == parent.childCount()-1

        self.blockSignals(True)

        if isLast and not item.isEmpty():
            # 插入空行
            print(item.data(0,0))
            TaskTreeNode(item, ['',''])
            TaskTreeNode(parent if parent else self, ['', ''])
        
        if item.isEmpty() and not isLast:
            if parent:
                parent.takeChild(parent.indexOfChild(item))
            else:
                self.takeTopLevelItem(self.indexOfTopLevelItem(item))

        self.blockSignals(False)
        return

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

        #return ItemWidget(parent)

        #return super().createEditor(parent, option, index)

        return QLineEdit(parent)

    def setModelData(self, editor: PySide2.QtWidgets.QWidget, model: QtCore.QAbstractItemModel, index: QtCore.QModelIndex) -> None:
        model.setData(index, editor.text())
        return

    # 通过重载下面两个函数，可实现自定义样式的绘制
    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex) -> None:
        return super().paint(painter, option, index)

        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)
        rect:QtCore.QRect = option.rect

        y = int(0.5*rect.height() + rect.y())
        painter.drawLine(rect.x(),y,rect.x()+rect.width(),y)
        return super().paint(painter, option, index)


    def editorEvent(self, event: PySide2.QtCore.QEvent, model: PySide2.QtCore.QAbstractItemModel, option: PySide2.QtWidgets.QStyleOptionViewItem, index: PySide2.QtCore.QModelIndex) -> bool:
        return super().editorEvent(event, model, option, index)
