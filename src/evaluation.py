import cv2
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QDialog

from src.fileController import FileController
from src.listWidgetItems import MyItem


class Evaluation(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.setWindowTitle("Data Display")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)  # 去除问号按钮
        layout = QVBoxLayout(self)

        # 添加一个标签到布局中
        self.label = QLabel("This is a Data Display", self)
        layout.addWidget(self.label)

    def actions(self):
        seg_label, num_segments = FileController.open_seg_label_of_human(self)
        # print("seg_label", seg_label)
        # 创建空白图像
        if not seg_label:
            print("close")
            return
        height = len(seg_label)
        width = len(seg_label[0])
        segmented_img = np.zeros((len(seg_label), len(seg_label[0]), 3), dtype=np.uint8)
        # 设置区域颜色
        colors = np.random.randint(0, 255, size=(num_segments, 3), dtype=np.uint8)
        for i in range(height):
            for j in range(width):
                segmented_img[i][j] = colors[seg_label[i][j]]
        cv2.imshow("Segmented Image", segmented_img)

        self.label.setText(str(self.calculate_compactness(MyItem.img_label)))
        # print(self.calculate_undersegmentation_error(seg_label, MyItem.img_label))
        # print(self.Undersegmentation_error(seg_label, MyItem.img_label))

    def calculate_compactness(self, segmented_labels):
        compactness = []
        for label in np.unique(segmented_labels):
            mask = (segmented_labels == label)
            contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            perimeter = cv2.arcLength(contours[0], closed=True)
            area = np.sum(mask)
            compactness.append(perimeter ** 2 / (4 * np.pi * area))
        return np.mean(compactness)

    def calculate_undersegmentation_error(self, true_labels, segmented_labels):
        ue_count = 0
        for label in np.unique(true_labels):
            unique_segmented_labels, counts = np.unique(segmented_labels[true_labels == label], return_counts=True)
            ue_count += np.sum(counts) - np.max(counts)
        print(true_labels.size)
        # ue = ue_count / true_labels.size
        ue = 1
        return ue

    def Undersegmentation_error(self, segments_truth, segments):

        """
        segments_truth : matrix ground truth
        segments_slic : matrix of segments (SLIC for example)

        To calculate the proximity level of superpixels to image borders

        """

        S_truth = np.unique(segments_truth.flatten())
        results = []

        for gt in S_truth:
            St0 = segments_truth == gt
            UE = 0
            for i in np.unique(segments[St0]):
                in_border = (segments[St0] == i).sum()
                out_border = (segments == i).sum() - in_border
                UE += min(in_border, out_border)

            results.append(UE)
        N = segments_truth.shape[0] * segments_truth.shape[1]

        return np.sum(results) / N  # normalise

