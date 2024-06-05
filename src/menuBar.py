from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAction, QColorDialog

import src.listWidgetItems
from src.fileController import FileController
from src.listWidgetItems import GrayingItem, EdgeItem, GammaItem, SkimageSLICItem, OpenCVSLICItem, OpenCVSEEDSItem, \
    OpenCVLSCItem, SINItem, ERSItem
from utils.data import Data
from utils.icons import Icons
from utils.observer import Observer


class MenuBar(Observer, QtWidgets.QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.main_window = parent
        # self.setStyleSheet("QMenuBar { background-color: #F8F8F8; }")

        Data.add_observer(self)

        # 文件
        self.file_menu = QtWidgets.QMenu(self)
        self.file_menu.setObjectName("file_menu")
        self.file_menu.setTitle("文件")
        self.addAction(self.file_menu.menuAction())

        self.open_action = QtWidgets.QAction(self.main_window)
        self.open_action.setObjectName("open")
        self.open_action.setText("打开")
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self.open_file)
        self.open_action.setIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_DirOpenIcon))
        self.file_menu.addAction(self.open_action)

        self.saveas_action = QtWidgets.QAction(self.main_window)
        self.saveas_action.setObjectName("save_as")
        self.saveas_action.setText("另存为")
        self.saveas_action.setShortcut("Ctrl+S")
        self.saveas_action.setIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_DialogSaveButton))
        self.saveas_action.triggered.connect(self.save_photo)
        self.file_menu.addAction(self.saveas_action)

        self.save_label_action = QtWidgets.QAction(self.main_window)
        self.save_label_action.setObjectName("save_label")
        self.save_label_action.setText("保存分割数据")
        # self.save_label_action.setShortcut("Ctrl+S")
        self.save_label_action.setIcon(Icons.create_svg_icon(Icons.save_segment))
        # self.save_label_action.setIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_DialogSaveButton))
        self.save_label_action.triggered.connect(self.save_label)
        self.file_menu.addAction(self.save_label_action)

        self.exit_action = QtWidgets.QAction(self.main_window)
        self.exit_action.setObjectName("exit")
        self.exit_action.setText("退出")
        self.exit_action.setIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_DialogCloseButton))
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(self.main_window.close)
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
        self.basic_menu.setIcon(Icons.create_svg_icon(Icons.watermelon))
        self.image_menu.addAction(self.basic_menu.menuAction())

        self.graying_action = QtWidgets.QAction(self.main_window)
        self.graying_action.setObjectName("graying_action")
        self.graying_action.setText("灰度化")
        self.graying_action.triggered.connect(self.graying_action_handle)
        self.basic_menu.addAction(self.graying_action)

        self.edge_action = QtWidgets.QAction(self.main_window)
        self.edge_action.setObjectName("edge_action")
        self.edge_action.setText("边缘检测")
        self.edge_action.triggered.connect(self.edge_action_handle)
        self.basic_menu.addAction(self.edge_action)

        self.gamma_action = QtWidgets.QAction(self.main_window)
        self.gamma_action.setObjectName("gamma_action")
        self.gamma_action.setText("伽马校正")
        self.gamma_action.triggered.connect(self.gamma_action_handle)
        self.basic_menu.addAction(self.gamma_action)

        ## 超像素分割
        self.algorithm_menu = QtWidgets.QMenu(self)
        self.algorithm_menu.setObjectName("algorithm_menu")
        self.algorithm_menu.setTitle("超像素分割")
        self.algorithm_menu.setIcon(Icons.create_svg_icon(Icons.cherry))
        self.image_menu.addAction(self.algorithm_menu.menuAction())

        # self.Skimage_SLIC_action = QtWidgets.QAction(self.main_window)
        # self.Skimage_SLIC_action.setObjectName("Skimage_SLIC")
        # self.Skimage_SLIC_action.setText("Skimage-SLIC")
        # self.Skimage_SLIC_action.triggered.connect(self.Skimage_SLIC_action_handle)
        # self.algorithm_menu.addAction(self.Skimage_SLIC_action)

        self.OpenCV_SLIC_action = QtWidgets.QAction(self.main_window)
        self.OpenCV_SLIC_action.setObjectName("OpenCV_SLIC")
        self.OpenCV_SLIC_action.setText("SLIC")
        self.OpenCV_SLIC_action.triggered.connect(self.OpenCV_SLIC_action_handle)
        self.algorithm_menu.addAction(self.OpenCV_SLIC_action)

        self.OpenCV_SEEDS_action = QtWidgets.QAction(self.main_window)
        self.OpenCV_SEEDS_action.setObjectName("OpenCV_SEEDS")
        self.OpenCV_SEEDS_action.setText("SEEDS")
        self.OpenCV_SEEDS_action.triggered.connect(self.OpenCV_SEEDS_action_handle)
        self.algorithm_menu.addAction(self.OpenCV_SEEDS_action)

        self.OpenCV_LSC_action = QtWidgets.QAction(self.main_window)
        self.OpenCV_LSC_action.setObjectName("OpenCV_LSC")
        self.OpenCV_LSC_action.setText("LSC")
        self.OpenCV_LSC_action.triggered.connect(self.OpenCV_LSC_action_handle)
        self.algorithm_menu.addAction(self.OpenCV_LSC_action)

        self.algorithm_menu.addSeparator()

        self.SIN_action = QtWidgets.QAction(self.main_window)
        self.SIN_action.setObjectName("SIN")
        self.SIN_action.setText("SIN")
        self.SIN_action.triggered.connect(self.SIN_action_handle)
        self.algorithm_menu.addAction(self.SIN_action)

        self.algorithm_menu.addSeparator()

        self.ERS_action = QtWidgets.QAction(self.main_window)
        self.ERS_action.setObjectName("ERS")
        self.ERS_action.setText("ERS")
        self.ERS_action.triggered.connect(self.ERS_action_handle)
        self.algorithm_menu.addAction(self.ERS_action)

        # 效果评估
        self.evaluation_menu = QtWidgets.QMenu(self)
        self.evaluation_menu.setObjectName("evaluation_menu")
        self.evaluation_menu.setTitle("效果评估")
        self.addAction(self.evaluation_menu.menuAction())

        self.open_human_segment_action = QtWidgets.QAction(self.main_window)
        self.open_human_segment_action.setObjectName("open_human_segment")
        self.open_human_segment_action.setText("打开人工分割数据")
        self.open_human_segment_action.triggered.connect(self.open_human_segment_action_handle)
        self.evaluation_menu.addAction(self.open_human_segment_action)

        self.open_algorithm_segment_action = QtWidgets.QAction(self.main_window)
        self.open_algorithm_segment_action.setObjectName("open_algorithm_segment")
        self.open_algorithm_segment_action.setText("打开分割数据")
        self.open_algorithm_segment_action.triggered.connect(self.open_algorithm_segment_action_handle)
        self.evaluation_menu.addAction(self.open_algorithm_segment_action)

        self.evaluation_menu.addSeparator()

        self.compactness_action = QtWidgets.QAction(self.main_window)
        self.compactness_action.setObjectName("compactness")
        self.compactness_action.setText("紧凑度(CO)")
        self.compactness_action.triggered.connect(self.compactness_action_handle)
        self.compactness_action.setEnabled(False)
        self.evaluation_menu.addAction(self.compactness_action)

        self.undersegmentation_error_action = QtWidgets.QAction(self.main_window)
        self.undersegmentation_error_action.setObjectName("undersegmentation_error")
        self.undersegmentation_error_action.setText("欠分割误差(UE)")
        self.undersegmentation_error_action.triggered.connect(self.undersegmentation_error_action_handle)
        self.undersegmentation_error_action.setEnabled(False)
        self.evaluation_menu.addAction(self.undersegmentation_error_action)

        self.compute_boundary_recall_action = QtWidgets.QAction(self.main_window)
        self.compute_boundary_recall_action.setObjectName("boundary_recall")
        self.compute_boundary_recall_action.setText("边界召回率(BR)")
        self.compute_boundary_recall_action.triggered.connect(self.compute_boundary_recall_action_handle)
        self.compute_boundary_recall_action.setEnabled(False)
        self.evaluation_menu.addAction(self.compute_boundary_recall_action)

        self.compute_boundary_precision_action = QtWidgets.QAction(self.main_window)
        self.compute_boundary_precision_action.setObjectName("boundary_precision")
        self.compute_boundary_precision_action.setText("边界精度(BP)")
        self.compute_boundary_precision_action.triggered.connect(self.compute_boundary_precision_handle)
        self.compute_boundary_precision_action.setEnabled(False)
        self.evaluation_menu.addAction(self.compute_boundary_precision_action)

        self.achievable_segmentation_accuracy_action = QtWidgets.QAction(self.main_window)
        self.achievable_segmentation_accuracy_action.setObjectName("achievable_segmentation_accuracy")
        self.achievable_segmentation_accuracy_action.setText("可达分割精度(ASA)")
        self.achievable_segmentation_accuracy_action.triggered.connect(
            self.achievable_segmentation_accuracy_action_handle)
        self.achievable_segmentation_accuracy_action.setEnabled(False)
        self.evaluation_menu.addAction(self.achievable_segmentation_accuracy_action)

        self.evaluation_menu.addSeparator()

        self.save_evaluation_data_action = QtWidgets.QAction(self.main_window)
        self.save_evaluation_data_action.setObjectName("save_evaluation_data")
        self.save_evaluation_data_action.setText("保存评估数据")
        self.save_evaluation_data_action.triggered.connect(self.save_evaluation_data_handle)
        self.save_evaluation_data_action.setEnabled(False)
        self.evaluation_menu.addAction(self.save_evaluation_data_action)

        self.open_human_segment_image_action = QtWidgets.QAction(self.main_window)
        self.open_human_segment_image_action.setObjectName("open_human_segment")
        self.open_human_segment_image_action.setText("打开人工分割图")
        self.open_human_segment_image_action.triggered.connect(self.open_human_segment_image_action_handle)
        self.open_human_segment_image_action.setEnabled(False)
        self.evaluation_menu.addAction(self.open_human_segment_image_action)

        self.open_segment_image_action = QtWidgets.QAction(self.main_window)
        self.open_segment_image_action.setObjectName("open_segment")
        self.open_segment_image_action.setText("打开分割效果图")
        self.open_segment_image_action.triggered.connect(self.open_segment_image_action_handle)
        self.open_segment_image_action.setEnabled(False)
        self.evaluation_menu.addAction(self.open_segment_image_action)

        # 设置
        self.settings_menu = QtWidgets.QMenu(self)
        self.settings_menu.setObjectName("settings")
        self.settings_menu.setTitle("设置")
        self.addAction(self.settings_menu.menuAction())

        ## 工具栏
        self.tool_bar_menu = QtWidgets.QMenu(self)
        self.tool_bar_menu.setObjectName("tool_bar")
        self.tool_bar_menu.setTitle("工具栏")
        self.settings_menu.addAction(self.tool_bar_menu.menuAction())

        self.file_bar = QtWidgets.QAction("文件操作栏", self)
        self.file_bar.setCheckable(True)
        self.file_bar.triggered.connect(self.file_bar_action_handle)
        self.tool_bar_menu.addAction(self.file_bar)

        ## 视图
        self.view_menu = QtWidgets.QMenu(self)
        self.view_menu.setObjectName("view_menu")
        self.view_menu.setTitle("视图")
        self.settings_menu.addAction(self.view_menu.menuAction())

        self.dock_view = QtWidgets.QAction("已选操作", self)
        self.dock_view.setCheckable(True)
        self.dock_view.setChecked(True)
        self.dock_view.triggered.connect(self.dock_view_action_handle)
        self.view_menu.addAction(self.dock_view)

        ## 外观
        self.skin_menu = QtWidgets.QMenu(self)
        self.skin_menu.setObjectName("skin_menu")
        self.skin_menu.setTitle("外观")
        self.settings_menu.addAction(self.skin_menu.menuAction())

        self.canvas_color = QtWidgets.QAction("画布背景颜色", self)
        self.canvas_color.triggered.connect(self.canvas_color_action_handle)
        self.skin_menu.addAction(self.canvas_color)

        self.edge_color = QtWidgets.QAction("超像素边界颜色", self)
        self.edge_color.triggered.connect(self.edge_color_action_handle)
        self.skin_menu.addAction(self.edge_color)

        # 属性信息
        self.attribute_menu = QtWidgets.QMenu(self)
        self.attribute_menu.setObjectName("attribute_menu")
        self.attribute_menu.setTitle("属性")
        self.addAction(self.attribute_menu.menuAction())

        self.info_action = QtWidgets.QAction(self.main_window)
        self.info_action.setObjectName("image_info")
        self.info_action.setText("图片属性")
        self.info_action.triggered.connect(self.info_action_handle)
        self.info_action.setEnabled(False)
        self.attribute_menu.addAction(self.info_action)

    def open_file(self) -> None:
        src_img = FileController.open_file_dialog(self)
        if src_img is not None:
            self.main_window.change_image(src_img)
            self.info_action.setEnabled(True)

    def save_photo(self) -> None:
        self.main_window.graphicsView.save_current()

    def save_label(self) -> None:
        FileController.save_label(self)

    def graying_action_handle(self) -> None:
        func_item = GrayingItem()
        self.main_window.funcListWidget.add_used_function(func_item)

    def edge_action_handle(self) -> None:
        func_item = EdgeItem()
        self.main_window.funcListWidget.add_used_function(func_item)

    def gamma_action_handle(self) -> None:
        func_item = GammaItem()
        self.main_window.funcListWidget.add_used_function(func_item)

    def Skimage_SLIC_action_handle(self) -> None:
        func_item = SkimageSLICItem()
        self.main_window.funcListWidget.add_used_function(func_item)

    def OpenCV_SLIC_action_handle(self) -> None:
        func_item = OpenCVSLICItem()
        self.main_window.funcListWidget.add_used_function(func_item)

    def OpenCV_SEEDS_action_handle(self) -> None:
        func_item = OpenCVSEEDSItem()
        self.main_window.funcListWidget.add_used_function(func_item)

    def OpenCV_LSC_action_handle(self) -> None:
        func_item = OpenCVLSCItem()
        self.main_window.funcListWidget.add_used_function(func_item)

    def SIN_action_handle(self) -> None:
        func_item = SINItem()
        self.main_window.funcListWidget.add_used_function(func_item)

    def ERS_action_handle(self) -> None:
        func_item = ERSItem()
        self.main_window.funcListWidget.add_used_function(func_item)

    def open_human_segment_action_handle(self) -> None:
        self.main_window.evaluation.open_human_segment()

    def open_algorithm_segment_action_handle(self) -> None:
        self.main_window.evaluation.open_algorithm_segment()

    def compactness_action_handle(self) -> None:
        self.main_window.evaluation.calculate_compactness_handle()

    def undersegmentation_error_action_handle(self) -> None:
        self.main_window.evaluation.compute_undersegmentation_error_handle()

    def compute_boundary_recall_action_handle(self) -> None:
        self.main_window.evaluation.compute_boundary_recall_action_handle()

    def compute_boundary_precision_handle(self) -> None:
        self.main_window.evaluation.compute_boundary_precision_handle()

    def achievable_segmentation_accuracy_action_handle(self) -> None:
        self.main_window.evaluation.compute_achievable_segmentation_accuracy_handle()

    def save_evaluation_data_handle(self) -> None:
        self.main_window.evaluation.save_evaluation_data()

    def open_segment_image_action_handle(self) -> None:
        self.main_window.evaluation.open_segment_image()

    def open_human_segment_image_action_handle(self) -> None:
        self.main_window.evaluation.open_human_segment_image()

    # tool_bar
    def file_bar_action_handle(self, checked) -> None:
        sender = self.sender()
        if isinstance(sender, QAction):
            if checked:
                self.main_window.toolBar1.show()
            else:
                self.main_window.toolBar1.close()

    def dock_view_action_handle(self, checked) -> None:
        sender = self.sender()
        if isinstance(sender, QAction):
            if checked:
                self.main_window.dock_used.show()
            else:
                self.main_window.dock_used.close()
                self.main_window.dock_attr.close()

    def canvas_color_action_handle(self) -> None:
        color = QColorDialog.getColor()
        if color.isValid():
            # hex_color = color.name()
            self.main_window.graphicsView.setBackgroundBrush(color)
            print(color)
        else:
            print("没有选择颜色")

    def edge_color_action_handle(self) -> None:
        color = QColorDialog.getColor()
        if color.isValid():
            # hex_color = color.name()
            src.listWidgetItems.MyItem.edge_color = color
        else:
            print("没有选择颜色")

    # image info
    def info_action_handle(self) -> None:
        self.main_window.attribute.show_image_info()

    def update(self, value) -> None:
        if value:
            self.compactness_action.setEnabled(True)
            self.info_action.setEnabled(True)
            if Data.have_human_label:
                self.undersegmentation_error_action.setEnabled(True)
                self.compute_boundary_recall_action.setEnabled(True)
                self.compute_boundary_precision_action.setEnabled(True)
                self.achievable_segmentation_accuracy_action.setEnabled(True)
                self.save_evaluation_data_action.setEnabled(True)

    def check_menu_enable(self):
        if Data.have_img_label:
            self.update(True)
        if Data.have_segmented_img:
            self.open_segment_image_action.setEnabled(True)
        if Data.have_human_segmented_img:
            self.open_human_segment_image_action.setEnabled(True)
