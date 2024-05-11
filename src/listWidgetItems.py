import numpy as np
import cv2
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem

from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries

from utils.data import Data


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

    @staticmethod
    def change_img_label(img_label):
        Data.set_have_img_label_handle(True)
        Data.img_label = img_label
        Data.img_type = 0

        unique_labels, counts = np.unique(img_label, return_counts=True)
        Data.num_superpixels = len(unique_labels)

    @staticmethod
    def color_segments(img, segments):
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
        self._gamma = 100

    def __call__(self, img):
        gamma_table = [np.power(x / 255.0, self._gamma / 100) * 255.0 for x in range(256)]
        gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
        return cv2.LUT(img, gamma_table)


class SkimageSLICItem(MyItem):
    def __init__(self, parent=None):
        super(SkimageSLICItem, self).__init__(' Skimage-SLIC ', parent=parent)
        self._num_segments = 1000
        self._compactness = 10
        self._sigma = 1

        self._edge = True
        self._color_fill = True

    def __call__(self, img):
        # 执行 SLIC 超像素分割
        segments = slic(img, n_segments=self._num_segments, compactness=self._compactness, sigma=self._sigma)
        # 根据超像素的平均颜色对超像素进行着色

        result_img = img
        if self._color_fill:
            result_img = self.color_segments(img, segments)

        if self._edge:
            boundaries = mark_boundaries(result_img, segments, color=(0, 0, 0), mode='subpixel')
            result_img = (boundaries * 255).astype(np.uint8)

        return result_img


class OpenCVSLICItem(MyItem):
    def __init__(self, parent=None):
        super(OpenCVSLICItem, self).__init__(' OpenCV-SLIC ', parent=parent)
        self._algorithm = 0
        self._num_superpixels = 2000
        self._region_size = 20
        self._ruler = 20
        self._iterate_times = 10  # 迭代次数
        self._edge = False
        self._color_fill = False
        self.alg = [
            ('SLIC', cv2.ximgproc.SLIC),  # 使用所需的区域大小分割图像
            ('SLICO', cv2.ximgproc.SLICO),  # 使用自适应紧致因子进行优化
            ('MSLIC', cv2.ximgproc.MSLIC)]  # 使用流形方法进行优化，产生对内容更敏感的超像素

    def __call__(self, img):
        if not (self._color_fill or self._edge):
            return img
        slic = cv2.ximgproc.createSuperpixelSLIC(img, algorithm=self.alg[self._algorithm][1],
                                                 region_size=self._region_size, ruler=self._ruler)
        slic.iterate(self._iterate_times)
        label_slic = slic.getLabels()  # 获取超像素标签
        self.change_img_label(label_slic)
        result_img = img
        if self._color_fill:
            result_img = self.color_segments(img, label_slic)

        if self._edge:
            mask_slic = slic.getLabelContourMask()  # 获取Mask，超像素边缘Mask==1
            mask_inv_slic = cv2.bitwise_not(mask_slic)
            result_img = cv2.bitwise_and(result_img, result_img, mask=mask_inv_slic)  # 在原图上绘制超像素边界
        Data.use_algorithm = self.alg[self._algorithm][0]
        return result_img


class OpenCVSEEDSItem(MyItem):
    def __init__(self, parent=None):
        super(OpenCVSEEDSItem, self).__init__(' OpenCV-SEEDS ', parent=parent)
        self._num_superpixels = 2000  # 超像素数目
        self._num_levels = 15  # 块级别数
        self._prior = 3
        self._histogram_bins = 5
        self._double_step = True  # 重复两次
        self._iterate_times = 10
        self._edge = False
        self._color_fill = False

    def __call__(self, img):
        if not (self._color_fill or self._edge):
            return img
        # 初始化seeds项，注意图片长宽的顺序
        seeds = cv2.ximgproc.createSuperpixelSEEDS(img.shape[1], img.shape[0], img.shape[2], self._num_superpixels,
                                                   self._num_levels,
                                                   self._prior, self._histogram_bins, self._double_step)
        seeds.iterate(img, self._iterate_times)  # 输入图像大小必须与初始化形状相同，迭代次数为10
        label_seeds = seeds.getLabels()
        self.change_img_label(label_seeds)
        result_img = img
        if self._color_fill:
            result_img = self.color_segments(img, label_seeds)

        if self._edge:
            mask_seeds = seeds.getLabelContourMask()
            mask_inv_seeds = cv2.bitwise_not(mask_seeds)
            result_img = cv2.bitwise_and(result_img, result_img, mask=mask_inv_seeds)
        Data.use_algorithm = 'SEEDS'
        return result_img


class OpenCVLSCItem(MyItem):
    def __init__(self, parent=None):
        super(OpenCVLSCItem, self).__init__(' OpenCV-LSC ', parent=parent)
        self._region_size = 10
        self._ratio = 75
        self._iterate_times = 10
        self._edge = False
        self._color_fill = False

    def __call__(self, img):
        if not (self._color_fill or self._edge):
            return img
        lsc = cv2.ximgproc.createSuperpixelLSC(img, self._region_size, self._ratio / 1000.0)
        lsc.iterate(self._iterate_times)
        label_lsc = lsc.getLabels()
        self.change_img_label(label_lsc)
        result_img = img
        if self._color_fill:
            result_img = self.color_segments(img, label_lsc)

        if self._edge:
            mask_lsc = lsc.getLabelContourMask()
            mask_inv_lsc = cv2.bitwise_not(mask_lsc)
            result_img = cv2.bitwise_and(result_img, result_img, mask=mask_inv_lsc)
        Data.use_algorithm = 'LSC'
        return result_img
