import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QMainWindow, QVBoxLayout, QLabel, QWidget, QGridLayout

from src.listWidgetItems import MyItem
from utils.data import Data


class Attribute(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent

        self.width_label = QLabel()
        self.height_label = QLabel()
        self.num_superpixels_label = QLabel()
        self.algorithm_label = QLabel()

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QGridLayout(self.centralWidget)
        self.layout.setVerticalSpacing(1)  # 设置垂直间距
        self.layout.setContentsMargins(10, 30, 10, 30)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinimizeButtonHint)
        self.setWindowTitle('属性')
        self.setFixedWidth(200)
        self.setFixedHeight(150)

    def show_image_info(self):
        have_img_label = Data.have_img_label
        self.width_label.setText("图片宽度: {}".format(Data.width))
        self.height_label.setText("图片高度: {}".format(Data.height))
        if have_img_label and Data.use_algorithm != '':
            self.setFixedHeight(150)
            self.algorithm_label.setText("分割算法: {}".format(Data.use_algorithm))
            Attribute.update_num_superpixels()
            self.num_superpixels_label.setText("超像素个数: {}".format(Data.num_superpixels))
            self.layout.addWidget(self.algorithm_label, 2, 0)
            self.layout.addWidget(self.num_superpixels_label, 3, 0)
        else:
            self.setFixedHeight(120)

        self.layout.addWidget(self.width_label, 0, 0)
        self.layout.addWidget(self.height_label, 1, 0)

        def set_labels_properties(labels):
            for lab in labels:
                lab.setStyleSheet("font-size: 20px;")
                lab.setTextInteractionFlags(Qt.TextSelectableByMouse)
                lab.setCursor(Qt.IBeamCursor)

        set_labels_properties([self.width_label, self.height_label, self.num_superpixels_label, self.algorithm_label])
        self.main_window.attribute.show()

    @staticmethod
    def update_num_superpixels():
        if Data.use_algorithm != '':
            label = Data.img_label
            unique_labels, counts = np.unique(label, return_counts=True)
            Data.num_superpixels = len(unique_labels)
