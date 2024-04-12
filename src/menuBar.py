from PyQt5 import QtCore, QtGui, QtWidgets

from src.fileController import FileController
from src.listWidgetItems import GrayingItem, EdgeItem, GammaItem, SkimageSLICItem, OpenCVSLICItem


class MenuBar(QtWidgets.QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.mainwindow = parent

        # self.menubar = QtWidgets.QMenuBar(self.mainwindow)
        # self.setGeometry(QtCore.QRect(0, 0, 800, 26))
        # self.menubar.setObjectName("menubar")
        # self.mainwindow.setMenuBar(self.menubar)

        # 文件

        self.file_menu = QtWidgets.QMenu(self)
        self.file_menu.setObjectName("file_menu")
        self.file_menu.setTitle("文件")
        self.addAction(self.file_menu.menuAction())

        self.open_action = QtWidgets.QAction(self.mainwindow)
        self.open_action.setObjectName("open")
        self.open_action.setText("打开")
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self.open_file)
        # icon3 = QtGui.QIcon()
        # icon3.addPixmap(QtGui.QPixmap(":/images/res/images/import.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # icon = QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_FileIcon)
        # self.open_action.setIcon(icon3)
        self.file_menu.addAction(self.open_action)

        self.saveas_action = QtWidgets.QAction(self.mainwindow)
        self.saveas_action.setObjectName("save_as")
        self.saveas_action.setText("另存为")
        self.saveas_action.setShortcut("Ctrl+S")
        self.saveas_action.triggered.connect(self.save_photo)
        self.file_menu.addAction(self.saveas_action)

        self.exit_action = QtWidgets.QAction(self.mainwindow)
        self.exit_action.setObjectName("exit")
        self.exit_action.setText("退出")
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(self.mainwindow.close)
        self.file_menu.addAction(self.exit_action)

        # 图像

        self.image_menu = QtWidgets.QMenu(self)
        self.image_menu.setObjectName("image_menu")
        self.image_menu.setTitle("图像")
        self.addAction(self.image_menu.menuAction())

        ## 图像操作

        self.basic_menu = QtWidgets.QMenu(self)
        self.basic_menu.setObjectName("basic_menu")
        self.basic_menu.setTitle("图像操作")
        self.image_menu.addAction(self.basic_menu.menuAction())

        self.graying_action = QtWidgets.QAction(self.mainwindow)
        self.graying_action.setObjectName("graying_action")
        self.graying_action.setText("灰度化")
        self.graying_action.triggered.connect(self.graying_action_handle)
        self.basic_menu.addAction(self.graying_action)

        self.edge_action = QtWidgets.QAction(self.mainwindow)
        self.edge_action.setObjectName("edge_action")
        self.edge_action.setText("边缘检测")
        self.edge_action.triggered.connect(self.edge_action_handle)
        self.basic_menu.addAction(self.edge_action)

        self.gramma_action = QtWidgets.QAction(self.mainwindow)
        self.gramma_action.setObjectName("gramma_action")
        self.gramma_action.setText("伽马校正")
        self.gramma_action.triggered.connect(self.gramma_action_handle)
        self.basic_menu.addAction(self.gramma_action)

        ## 超像素分割

        self.algorithm_menu = QtWidgets.QMenu(self)
        self.algorithm_menu.setObjectName("algorithm_menu")
        self.algorithm_menu.setTitle("超像素分割")
        self.image_menu.addAction(self.algorithm_menu.menuAction())

        self.Skimage_SLIC_action = QtWidgets.QAction(self.mainwindow)
        self.Skimage_SLIC_action.setObjectName("Skimage_SLIC")
        self.Skimage_SLIC_action.setText("Skimage-SLIC")
        self.Skimage_SLIC_action.triggered.connect(self.Skimage_SLIC_action_handle)
        self.algorithm_menu.addAction(self.Skimage_SLIC_action)

        self.OpenCV_SLIC_action = QtWidgets.QAction(self.mainwindow)
        self.OpenCV_SLIC_action.setObjectName("OpenCV_SLIC")
        self.OpenCV_SLIC_action.setText("OpenCV-SLIC")
        self.OpenCV_SLIC_action.triggered.connect(self.OpenCV_SLIC_action_handle)
        self.algorithm_menu.addAction(self.OpenCV_SLIC_action)


        # QtCore.QMetaObject.connectSlotsByName(self.mainwindow)

    def open_file(self) -> None:
        self.file_open = FileController(self)
        src_img = self.file_open.open_file_dialog(self)
        if src_img is not None:
            self.mainwindow.change_image(src_img)
        print("openfile")

    def save_photo(self) -> None:
        self.mainwindow.graphicsView.save_current()

    def graying_action_handle(self) -> None:
        func_item = GrayingItem()
        self.mainwindow.funcListWidget.add_used_function(func_item)

    def edge_action_handle(self) -> None:
        func_item = EdgeItem()
        self.mainwindow.funcListWidget.add_used_function(func_item)

    def gramma_action_handle(self) -> None:
        func_item = GammaItem()
        self.mainwindow.funcListWidget.add_used_function(func_item)

    def Skimage_SLIC_action_handle(self) -> None:
        func_item = SkimageSLICItem()
        self.mainwindow.funcListWidget.add_used_function(func_item)

    def OpenCV_SLIC_action_handle(self) -> None:
        func_item = OpenCVSLICItem()
        self.mainwindow.funcListWidget.add_used_function(func_item)
