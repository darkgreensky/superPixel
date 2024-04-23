import numpy as np
from PyQt5.QtWidgets import QDialog

from src.listWidgetItems import MyItem
from utils.data import Data


class Attribute(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.height = 0
        self.width = 0
        self.num_superpixels = 0

    def get_image_info(self):
        label = Data.img_label
        have_img_label = Data.have_img_label
        src_img = self.main_window.src_img
        have_image = True
        if src_img is None:
            have_image = False

        if have_image:
            self.height, self.width = src_img.shape[:2]
            print("图片宽度", self.width)
            print("图片高度", self.height)
        if have_img_label:
            unique_labels, counts = np.unique(label, return_counts=True)
            self.num_superpixels = len(unique_labels)
            print("超像素个数", self.num_superpixels)
