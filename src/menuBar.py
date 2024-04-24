from PyQt5 import QtCore, QtGui, QtWidgets

from src.fileController import FileController
from src.listWidgetItems import GrayingItem, EdgeItem, GammaItem, SkimageSLICItem, OpenCVSLICItem, OpenCVSEEDSItem, \
    OpenCVLSCItem
from utils.data import Data
from utils.icons import Icons
from utils.observer import Observer


class MenuBar(Observer, QtWidgets.QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.main_window = parent

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
        self.OpenCV_SLIC_action.setText("OpenCV-SLIC")
        self.OpenCV_SLIC_action.triggered.connect(self.OpenCV_SLIC_action_handle)
        self.algorithm_menu.addAction(self.OpenCV_SLIC_action)

        self.OpenCV_SEEDS_action = QtWidgets.QAction(self.main_window)
        self.OpenCV_SEEDS_action.setObjectName("OpenCV_SEEDS")
        self.OpenCV_SEEDS_action.setText("OpenCV-SEEDS")
        self.OpenCV_SEEDS_action.triggered.connect(self.OpenCV_SEEDS_action_handle)
        self.algorithm_menu.addAction(self.OpenCV_SEEDS_action)

        self.OpenCV_LSC_action = QtWidgets.QAction(self.main_window)
        self.OpenCV_LSC_action.setObjectName("OpenCV_LSC")
        self.OpenCV_LSC_action.setText("OpenCV-LSC")
        self.OpenCV_LSC_action.triggered.connect(self.OpenCV_LSC_action_handle)
        self.algorithm_menu.addAction(self.OpenCV_LSC_action)

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

        self.compactness_action = QtWidgets.QAction(self.main_window)
        self.compactness_action.setObjectName("compactness")
        self.compactness_action.setText("紧凑度")
        self.compactness_action.triggered.connect(self.compactness_action_handle)
        self.compactness_action.setEnabled(False)
        self.evaluation_menu.addAction(self.compactness_action)

        self.undersegmentation_error_action = QtWidgets.QAction(self.main_window)
        self.undersegmentation_error_action.setObjectName("undersegmentation_error")
        self.undersegmentation_error_action.setText("欠分割误差")
        self.undersegmentation_error_action.triggered.connect(self.undersegmentation_error_action_handle)
        self.undersegmentation_error_action.setEnabled(False)
        self.evaluation_menu.addAction(self.undersegmentation_error_action)

        self.compute_boundary_recall_action = QtWidgets.QAction(self.main_window)
        self.compute_boundary_recall_action.setObjectName("boundary_recall")
        self.compute_boundary_recall_action.setText("边界召回率")
        self.compute_boundary_recall_action.triggered.connect(self.compute_boundary_recall_action_handle)
        self.compute_boundary_recall_action.setEnabled(False)
        self.evaluation_menu.addAction(self.compute_boundary_recall_action)

        self.compute_boundary_precision_action = QtWidgets.QAction(self.main_window)
        self.compute_boundary_precision_action.setObjectName("boundary_precision")
        self.compute_boundary_precision_action.setText("边界精度")
        self.compute_boundary_precision_action.triggered.connect(self.compute_boundary_precision_handle)
        self.compute_boundary_precision_action.setEnabled(False)
        self.evaluation_menu.addAction(self.compute_boundary_precision_action)

        self.achievable_segmentation_accuracy_action = QtWidgets.QAction(self.main_window)
        self.achievable_segmentation_accuracy_action.setObjectName("achievable_segmentation_accuracy")
        self.achievable_segmentation_accuracy_action.setText("可达分割精度")
        self.achievable_segmentation_accuracy_action.triggered.connect(
            self.achievable_segmentation_accuracy_action_handle)
        self.achievable_segmentation_accuracy_action.setEnabled(False)
        self.evaluation_menu.addAction(self.achievable_segmentation_accuracy_action)

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
