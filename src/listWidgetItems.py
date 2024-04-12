import numpy as np
import cv2
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QListWidgetItem, QPushButton
# from utils.flags import *

from skimage.segmentation import slic

class MyItem(QListWidgetItem):
    def __init__(self, name=None, parent=None):
        super(MyItem, self).__init__(name, parent=parent)
        self.setIcon(QIcon('icons/color.png'))
        self.setSizeHint(QSize(60, 60))  # size

    def get_params(self):
        protected = [v for v in dir(self) if v.startswith('_') and not v.startswith('__')]
        param = {}
        for v in protected:
            param[v.replace('_', '', 1)] = self.__getattribute__(v)
        return param

    def update_params(self, param):
        for k, v in param.items():
            if '_' + k in dir(self):
                self.__setattr__('_' + k, v)


class GrayingItem(MyItem):
    def __init__(self, parent=None):
        super(GrayingItem, self).__init__(' 灰度化 ', parent=parent)
        self._mode = 0

    def __call__(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img


class EdgeItem(MyItem):
    def __init__(self, parent=None):
        super(EdgeItem, self).__init__('边缘检测', parent=parent)
        self._thresh1 = 20
        self._thresh2 = 100

    def __call__(self, img):
        img = cv2.Canny(img, threshold1=self._thresh1, threshold2=self._thresh2)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img


class GammaItem(MyItem):
    def __init__(self, parent=None):
        super(GammaItem, self).__init__('伽马校正', parent=parent)
        self._gamma = 1

    def __call__(self, img):
        gamma_table = [np.power(x / 255.0, self._gamma) * 255.0 for x in range(256)]
        gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
        return cv2.LUT(img, gamma_table)


class SkimageSLICItem(MyItem):
    def __init__(self, parent=None):
        super(SkimageSLICItem, self).__init__(' Skimage-SLIC ', parent=parent)
        self._num_segments = 1000
        self._compactness = 10
        self._sigma = 1
        """
        参数:
            num_segments (int): 期望的超像素数量。
            compactness (float): 紧凑度参数。较高的值会产生更加空间紧凑的超像素。
            sigma (float): 高斯平滑的标准差。
        """

    def __call__(self, img):
        """
        使用 SLIC 算法对输入图像进行超像素分割。

        参数:
            img (numpy.ndarray): 输入图像。

        返回:
            segmented_img (numpy.ndarray): 分割后的图像。
            segments (numpy.ndarray): 每个像素对应的超像素标识数组。
        """
        # 执行 SLIC 超像素分割
        segments = slic(img, n_segments=self._num_segments, compactness=self._compactness, sigma=self._sigma)
        # 根据超像素的平均颜色对超像素进行着色
        segmented_img = self.color_segments(img, segments)

        return segmented_img
        # segments

    def color_segments(self, img, segments):
        """
        根据超像素的平均颜色对超像素进行着色。

        参数:
            img (numpy.ndarray): 输入图像。
            segments (numpy.ndarray): 每个像素对应的超像素标识数组。

        返回:
            segmented_img (numpy.ndarray): 分割后的图像。
        """
        # 创建输入图像的副本
        segmented_img = img.copy()

        # 计算每个超像素的平均颜色
        colors = []
        for i in range(segments.max() + 1):
            # 检查超像素是否为空
            if np.any(segments == i):
                colors.append(img[segments == i].mean(axis=0))
            else:
                # 超像素为空，将其颜色设为黑色或者其他默认颜色
                colors.append([255, 255, 255])  # 白色

        # 将每个像素分配到其对应的超像素的平均颜色上
        for i in range(min(segments.max() + 1, len(colors))):
            if np.any(segmented_img[segments == i]):
                segmented_img[segments == i] = colors[i]
        return segmented_img

class OpenCVSLICItem(MyItem):
    def __init__(self, parent=None):
        super(OpenCVSLICItem, self).__init__(' OpenCV-SLIC ', parent=parent)
        self._algorithm = 0
        self._region_size = 20
        self._ruler = 20
        self._edge = False
        self._color_fill = True
        self.alg = [
        ('SLIC', cv2.ximgproc.SLIC),  # 使用所需的区域大小分割图像
        ('SLICO', cv2.ximgproc.SLICO),  # 使用自适应紧致因子进行优化
        ('MSLIC', cv2.ximgproc.MSLIC)]  # 使用流形方法进行优化，产生对内容更敏感的超像素

    def __call__(self, img):
        image_lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        slic = cv2.ximgproc.createSuperpixelSLIC(image_lab,algorithm=self.alg[self._algorithm][1],
                                                 region_size=self._region_size, ruler=self._ruler)
        # slic = cv2.ximgproc.createSuperpixelSLIC(image_lab, region_size=20, ruler=20.0)
        slic.iterate(100)
        label_slic = slic.getLabels()  # 获取超像素标签
        number_slic = slic.getNumberOfSuperpixels()  # 获取超像素数目

        segmented_img = img
        if self._color_fill:
            segmented_img = self.color_segments(img, label_slic)

        if self._edge:
            mask_slic = slic.getLabelContourMask()  # 获取Mask，超像素边缘Mask==1
            mask_inv_slic = cv2.bitwise_not(mask_slic)
            segmented_img = cv2.bitwise_and(segmented_img, segmented_img, mask=mask_inv_slic)  # 在原图上绘制超像素边界

        return segmented_img

    def color_segments(self, img, segments):
        """
        根据超像素的平均颜色对超像素进行着色。

        参数:
            img (numpy.ndarray): 输入图像。
            segments (numpy.ndarray): 每个像素对应的超像素标识数组。

        返回:
            segmented_img (numpy.ndarray): 分割后的图像。
        """
        # 创建输入图像的副本
        segmented_img = img.copy()

        # 计算每个超像素的平均颜色
        colors = []
        for i in range(segments.max() + 1):
            # 检查超像素是否为空
            if np.any(segments == i):
                colors.append(img[segments == i].mean(axis=0))
            else:
                # 超像素为空，将其颜色设为黑色或者其他默认颜色
                colors.append([255, 255, 255])  # 白色

        # 将每个像素分配到其对应的超像素的平均颜色上
        for i in range(min(segments.max() + 1, len(colors))):
            if np.any(segmented_img[segments == i]):
                segmented_img[segments == i] = colors[i]
        return segmented_img
