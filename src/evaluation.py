import cv2
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QDialog, QMessageBox

from src.fileController import FileController
from src.listWidgetItems import MyItem
from utils.data import Data


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

    def open_human_segment(self):
        true_label, num_segments, segmented_img = FileController.open_seg_label_of_human(self)
        if true_label is None:
            print("close")
            return
        Data.update_human_img_info(true_label, num_segments, True, segmented_img)
        self.main_window.menu.open_human_segment_image_action.setEnabled(True)
        self.check_menu_enable()
        cv2.imshow("Human Segment Image", segmented_img)

    def open_algorithm_segment(self):
        true_label, num_segments, segmented_img = FileController.open_seg_label_of_algorithm(self)
        if true_label is None:
            print("close")
            return
        Data.update_img_info(true_label, num_segments, True, segmented_img)
        self.main_window.menu.open_segment_image_action.setEnabled(True)
        self.check_menu_enable()
        cv2.imshow("Segment Image", segmented_img)

# ----------------------------------------------------------------------------------------------------------------------
#       compactness 紧凑度
# ----------------------------------------------------------------------------------------------------------------------

    def calculate_compactness_handle(self):
        print(self.calculate_compactness(Data.img_label))
        # self.label.setText(str(self.calculate_compactness(Data.img_label)))

    def calculate_compactness(self, segmented_labels):
        compactness = []
        for label in np.unique(segmented_labels):
            mask = (segmented_labels == label)
            contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            perimeter = cv2.arcLength(contours[0], closed=True)
            area = np.sum(mask)
            compactness.append(perimeter ** 2 / (4 * np.pi * area))
        return np.mean(compactness)

# ----------------------------------------------------------------------------------------------------------------------
#       undersegmentation_error  欠分割误差
# ----------------------------------------------------------------------------------------------------------------------

    def compute_undersegmentation_error_handel(self):
        if Data.have_img_label and Data.have_human_label:
            self.compute_undersegmentation_error(Data.img_label, Data.human_label)
        else:
            if Data.have_img_label is False and Data.have_human_label is False:
                QMessageBox.information(self, "提示", "缺少图片分割数据和人工分割数据",
                                        QMessageBox.Yes)
            elif Data.have_img_label is False:
                QMessageBox.information(self, "提示", "缺少图片分割数据",
                                        QMessageBox.Yes)
            elif Data.have_human_label is False:
                QMessageBox.information(self, "提示", "未导入人工分割数据",
                                        QMessageBox.Yes)
            else:
                QMessageBox.information(self, "提示", "异常错误",
                                        QMessageBox.Yes)

    def compute_intersection_matrix(self, labels, gt):
        if labels.shape != gt.shape:
            print("Superpixel segmentation does not match ground truth size.")
            return None, None, None

        superpixels = np.max(labels) + 1
        gt_segments = np.max(gt) + 1

        superpixel_sizes = np.zeros(superpixels, dtype=int)
        gt_sizes = np.zeros(gt_segments, dtype=int)

        intersection_matrix = np.zeros((gt_segments, superpixels), dtype=int)

        for i in range(labels.shape[0]):
            for j in range(labels.shape[1]):
                intersection_matrix[gt[i, j], labels[i, j]] += 1
                superpixel_sizes[labels[i, j]] += 1
                gt_sizes[gt[i, j]] += 1

        return intersection_matrix, superpixel_sizes, gt_sizes

    def compute_undersegmentation_error(self, labels, gt):
        if labels.shape != gt.shape:
            print("Superpixel segmentation does not match ground truth size.")
            return None

        H, W = gt.shape
        N = H * W

        intersection_matrix, superpixel_sizes, gt_sizes = self.compute_intersection_matrix(labels, gt)

        if intersection_matrix is None:
            return None

        error = 0
        for j in range(intersection_matrix.shape[1]):
            min_diff = np.inf
            for i in range(intersection_matrix.shape[0]):
                superpixel_j_minus_gt_i = superpixel_sizes[j] - intersection_matrix[i, j]
                if superpixel_j_minus_gt_i < 0:
                    print("Set difference is negative.")
                if superpixel_j_minus_gt_i < min_diff:
                    min_diff = superpixel_j_minus_gt_i

            error += min_diff
        print(error / N)
        return error / N

    #     def calculate_undersegmentation_error(self, true_labels, segmented_labels):
    #         ue_count = 0
    #         for label in np.unique(true_labels):
    #             unique_segmented_labels, counts = np.unique(segmented_labels[true_labels == label], return_counts=True)
    #             ue_count += np.sum(counts) - np.max(counts)
    #         print(true_labels.size)
    #         ue = ue_count / true_labels.size
    #         ue = 1
    #         return ue

# ----------------------------------------------------------------------------------------------------------------------
#       boundary_recall 边缘召回率
# ----------------------------------------------------------------------------------------------------------------------

    def compute_boundary_recall_action_handel(self):
        print(self.compute_boundary_recall(Data.img_label, Data.human_label, 0.0025))

    def compute_boundary_recall(self, labels, gt, d: float):
        if labels.shape != gt.shape:
            raise ValueError("Superpixel segmentation does not match ground truth size.")

        H, W = gt.shape
        r = int(round(d * np.sqrt(H * H + W * W)))
        # print("r", r)
        tp = 0
        fn = 0

        for i in range(H):
            # print(i, H)
            for j in range(W):
                if self.is_4_connected_boundary_pixel(gt, i, j):
                    pos = False
                    for k in range(max(0, i - r), min(H - 1, i + r) + 1):
                        for l in range(max(0, j - r), min(W - 1, j + r) + 1):
                            if self.is_4_connected_boundary_pixel(labels, k, l):
                                pos = True
                    if pos:
                        tp += 1
                    else:
                        fn += 1
                    # print("tp fn:", tp, fn)

        if tp + fn > 0:
            return tp / (tp + fn)
        return 0

    def is_4_connected_boundary_pixel(self, labels, i, j):
        if i > 0:
            if labels[i, j] != labels[i - 1, j]:
                return True

        if i < labels.shape[0] - 1:
            if labels[i, j] != labels[i + 1, j]:
                return True

        if j > 0:
            if labels[i, j] != labels[i, j - 1]:
                return True

        if j < labels.shape[1] - 1:
            if labels[i, j] != labels[i, j + 1]:
                return True

        return False

# ----------------------------------------------------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------------------------------------------------

    def open_human_segment_image(self):
        if Data.have_human_segmented_img:
            cv2.imshow("Human Segment Image", Data.human_segmented_img)

    def open_segment_image(self):
        if Data.have_segmented_img:
            cv2.imshow("Segment Image", Data.segmented_img)

    def check_menu_enable(self):
        if Data.have_img_label:
            self.main_window.menu.compactness_action.setEnabled(True)
            if Data.have_human_label:
                self.main_window.menu.undersegmentation_error_action.setEnabled(True)
                self.main_window.menu.compute_boundary_recall_action.setEnabled(True)
