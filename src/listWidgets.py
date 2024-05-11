from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QListWidget, QListView, QAbstractItemView, QMenu, QAction

from utils.config import items


class MyListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.main_window = parent
        self.setDragEnabled(True)
        # 选中不显示虚线
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)


class UsedListWidget(MyListWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setAcceptDrops(True)
        self.setFlow(QListView.TopToBottom)  # 设置列表方向
        self.setDefaultDropAction(Qt.MoveAction)  # 设置拖放为移动而不是复制一个
        self.setDragDropMode(QAbstractItemView.InternalMove)  # 设置拖放模式, 内部拖放
        self.itemClicked.connect(self.show_attr)
        self.setMinimumWidth(280)

        self.move_item = None

    def contextMenuEvent(self, e):
        # 右键菜单事件
        item = self.itemAt(self.mapFromGlobal(QCursor.pos()))
        if not item:
            return  # 判断是否是空白区域
        menu = QMenu()
        delete_action = QAction('删除', self)
        delete_action.triggered.connect(lambda: self.delete_item(item))  # 传递额外值
        menu.addAction(delete_action)
        menu.exec(QCursor.pos())

    def delete_item(self, item):
        # 删除操作
        self.takeItem(self.row(item))
        self.main_window.update_image()  # 更新frame
        self.main_window.dock_attr.close()

    def dropEvent(self, event):
        if self.count() <= 1:
            return
        # have bug
        super().dropEvent(event)
        self.main_window.update_image()

    def show_attr(self):
        item = self.itemAt(self.mapFromGlobal(QCursor.pos()))
        if not item:
            return
        try:
            param = item.get_params()  # 获取当前item的属性
            if type(item) in items:
                index = items.index(type(item))  # 获取item对应的table索引
                self.main_window.stackedWidget.setCurrentIndex(index)
                self.main_window.stackedWidget.currentWidget().update_params(param)  # 更新对应的table
                self.main_window.dock_attr.show()
        except Exception as e:
            print(e)



class FuncListWidget(MyListWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.close()

    def add_used_function(self, func_item):
        # func_item = self.currentItem()
        if type(func_item) in items:
            use_item = type(func_item)()
            self.main_window.useListWidget.addItem(use_item)
            self.main_window.update_image()
