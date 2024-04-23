import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QMainWindow, QVBoxLayout, QLabel, QWidget, QGridLayout

from src.listWidgetItems import MyItem
from utils.data import Data


class Attribute(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent

        self.height = 0
        self.width = 0
        self.num_superpixels = 0

        self.width_label = QLabel()
        self.height_label = QLabel()
        self.num_superpixels_label = QLabel()

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QGridLayout(self.centralWidget)
        self.layout.setVerticalSpacing(1)  # 设置垂直间距
        self.layout.setContentsMargins(10, 30, 10, 30)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinimizeButtonHint)
        self.setWindowTitle('属性')
        self.setFixedWidth(200)
        self.setFixedHeight(120)

    def get_image_info(self):
        label = Data.img_label
        have_img_label = Data.have_img_label
        src_img = self.main_window.src_img
        have_image = True
        if src_img is None:
            have_image = False
        if have_image:
            self.height, self.width = src_img.shape[:2]
            self.width_label.setText("图片宽度: {}".format(self.width))
            self.height_label.setText("图片高度: {}".format(self.height))
        if have_img_label:
            unique_labels, counts = np.unique(label, return_counts=True)
            self.num_superpixels = len(unique_labels)
            self.num_superpixels_label.setText("超像素个数: {}".format(self.num_superpixels))

        self.layout.addWidget(self.width_label, 0, 0)
        self.layout.addWidget(self.height_label, 1, 0)
        self.layout.addWidget(self.num_superpixels_label, 2, 0)

        def set_labels_properties(labels):
            for lab in labels:
                lab.setStyleSheet("font-size: 20px;")
                lab.setTextInteractionFlags(Qt.TextSelectableByMouse)
                lab.setCursor(Qt.IBeamCursor)

        set_labels_properties([self.width_label, self.height_label, self.num_superpixels_label])

        self.main_window.attribute.show()
