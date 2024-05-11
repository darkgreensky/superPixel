from PyQt5 import QtWidgets
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QToolBar, QAction

from utils.icons import Icons


class ToolBar(QToolBar):
    def __init__(self, parent=None):
        super(ToolBar, self).__init__()
        self.main_window = parent
        self.setMaximumHeight(30)

        self.open_action = QAction(self)
        self.addAction(self.open_action)
        self.open_action.setIcon(Icons.create_svg_icon(Icons.open_file))
        self.open_action.triggered.connect(self.main_window.menu.open_file)

        self.saveas_action = QAction(self)
        self.addAction(self.saveas_action)
        self.saveas_action.setIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_DialogSaveButton))
        self.saveas_action.triggered.connect(self.main_window.menu.save_photo)

        self.save_label_action = QAction(self)
        self.addAction(self.save_label_action)
        self.save_label_action.setIcon(Icons.create_svg_icon(Icons.save_segment))
        self.save_label_action.triggered.connect(self.main_window.menu.save_label)

        self.setMovable(True)
