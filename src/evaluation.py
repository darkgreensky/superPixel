import cv2
import numpy as np
from PyQt5.QtWidgets import QDialog, QMessageBox

from src.fileController import FileController
from utils.data import Data


class Evaluation(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent

    def open_human_segment(self):
        true_label, num_segments, segmented_img = FileController.open_seg_label_of_human(self)
        if true_label is None:
            return
        Data.update_human_img_info(true_label, num_segments, True, segmented_img)
        self.main_window.menu.check_menu_enable()
        cv2.imshow("Human Segment Image", segmented_img)

    def open_algorithm_segment(self):
        label, num_segments, segmented_img, \
            height, width, use_algorithm = FileController.open_seg_label_of_algorithm(self)
        if label is None:
            return
        Data.update_img_info(label, num_segments, 1, True, segmented_img, height, width, use_algorithm)
        self.main_window.menu.check_menu_enable()
        cv2.imshow("Segment Image", segmented_img)

    # ------------------------------------------------------------------------------------------------------------------
    #       compactness 紧凑度
    # ------------------------------------------------------------------------------------------------------------------

    def calculate_compactness_handle(self, message=True):
        res = self.calculate_compactness(Data.img_label)
        if message:
            self.main_window.messageBox.get_message("紧凑度: {:.6f}".format(res), "紧凑度")
        return res

    # def calculate_compactness(self, segmented_labels):
    #     compactness = []
    #     for label in np.unique(segmented_labels):
    #         mask = (segmented_labels == label)
    #         contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #         perimeter = cv2.arcLength(contours[0], closed=True)
    #         area = np.sum(mask)
    #         compactness.append(perimeter ** 2 / (4 * np.pi * area))
    #     return np.mean(compactness)

    def calculate_compactness(self, labels):
        superpixels = np.max(labels) + 1

        perimeter = np.zeros(superpixels)
        area = np.zeros(superpixels)

        for i in range(labels.shape[0]):
            for j in range(labels.shape[1]):
                count = 0

                if i > 0:
                    if labels[i, j] != labels[i - 1, j]:
                        count += 1
                else:
                    count += 1

                if i < labels.shape[0] - 1:
                    if labels[i, j] != labels[i + 1, j]:
                        count += 1
                else:
                    count += 1

                if j > 0:
                    if labels[i, j] != labels[i, j - 1]:
                        count += 1
                else:
                    count += 1

                if j < labels.shape[1] - 1:
                    if labels[i, j] != labels[i, j + 1]:
                        count += 1
                else:
                    count += 1

                perimeter[labels[i, j]] += count
                area[labels[i, j]] += 1

        compactness = 0

        for i in range(superpixels):
            if perimeter[i] > 0:
                compactness += area[i] * (4 * np.pi * area[i]) / (perimeter[i] * perimeter[i])

        compactness /= labels.size

        if compactness > 1.0:
            print("Invalid compactness:", compactness)

        return compactness

    # ------------------------------------------------------------------------------------------------------------------
    #       undersegmentation_error  欠分割误差
    # ------------------------------------------------------------------------------------------------------------------

    def compute_undersegmentation_error_handle(self, message=True):
        if Data.have_img_label and Data.have_human_label:
            res = self.compute_undersegmentation_error(Data.img_label, Data.human_label)
            if message and res is not None:
                self.main_window.messageBox.get_message("欠分割误差: {:.6f}".format(res), "欠分割误差")
            return res
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
            return None

    def compute_intersection_matrix(self, labels, gt):
        if labels.shape != gt.shape:
            QMessageBox.critical(self, "错误", "Superpixel segmentation does not match ground truth size.",
                                 QMessageBox.Yes)
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
            QMessageBox.critical(self, "错误", "Superpixel segmentation does not match ground truth size.",
                                 QMessageBox.Yes)
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
        return error / N

    # ------------------------------------------------------------------------------------------------------------------
    #       boundary_recall 边界召回率
    # ------------------------------------------------------------------------------------------------------------------

    def compute_boundary_recall_action_handle(self, message=True):
        res = self.compute_boundary_recall(Data.img_label, Data.human_label, 0.0025)
        if message and res is not None:
            self.main_window.messageBox.get_message("边界召回率: {:.6f}".format(res), "边界召回率")
        return res

    def compute_boundary_recall(self, labels, gt, d: float):
        if labels.shape != gt.shape:
            QMessageBox.critical(self, "错误", "Superpixel segmentation does not match ground truth size.",
                                 QMessageBox.Yes)
            return None

        H, W = gt.shape
        r = int(round(d * np.sqrt(H * H + W * W)))
        tp = 0
        fn = 0

        for i in range(H):
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

        if tp + fn > 0:
            return tp / (tp + fn)
        return 0

    # ------------------------------------------------------------------------------------------------------------------
    #       boundary_precision 边界精度
    # ------------------------------------------------------------------------------------------------------------------

    def compute_boundary_precision_handle(self, message=True):
        res = self.compute_boundary_precision(Data.img_label, Data.human_label, 0.0025)
        if message and res is not None:
            self.main_window.messageBox.get_message("边界精度: {:.6f}".format(res), "边界精度")
        return res

    def compute_boundary_precision(self, labels, gt, d):
        if labels.shape != gt.shape:
            QMessageBox.critical(self, "错误", "Superpixel segmentation does not match ground truth size.",
                                 QMessageBox.Yes)
            return None
        H, W = gt.shape
        r = round(d * np.sqrt(H * H + W * W))

        tp = 0
        fp = 0

        for i in range(H):
            for j in range(W):
                if self.is_4_connected_boundary_pixel(gt, i, j):

                    pos = False
                    # Search for boundary pixel in the supervoxel segmentation.
                    for k in range(max(0, i - r), min(H - 1, i + r) + 1):
                        for l in range(max(0, j - r), min(W - 1, j + r) + 1):
                            if self.is_4_connected_boundary_pixel(labels, k, l):
                                pos = True

                    if pos:
                        tp += 1
                elif self.is_4_connected_boundary_pixel(labels, i, j):
                    pos = False
                    # Search for boundary pixel in the supervoxel segmentation.
                    for k in range(max(0, i - r), min(H - 1, i + r) + 1):
                        for l in range(max(0, j - r), min(W - 1, j + r) + 1):
                            if self.is_4_connected_boundary_pixel(gt, k, l):
                                pos = True

                    if not pos:
                        fp += 1

        if tp + fp > 0:
            return tp / (tp + fp)

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

    # ------------------------------------------------------------------------------------------------------------------
    #       achievable_segmentation_accuracy 可达分割精度
    # ------------------------------------------------------------------------------------------------------------------

    def compute_achievable_segmentation_accuracy_handle(self, message=True):
        res = self.compute_achievable_segmentation_accuracy(Data.img_label, Data.human_label)
        if message and res is not None:
            self.main_window.messageBox.get_message("可达分割精度: {:.6f}".format(res), "可达分割精度")
        return res

    def compute_achievable_segmentation_accuracy(self, labels, gt):
        if labels.shape != gt.shape:
            QMessageBox.critical(self, "错误", "Superpixel segmentation does not match ground truth size.",
                                 QMessageBox.Yes)
            return None

        H, W = gt.shape[:2]
        N = H * W

        intersection_matrix, superpixel_sizes, gt_sizes = self.compute_intersection_matrix(labels, gt)

        accuracy = 0
        for j in range(intersection_matrix.shape[1]):
            max_intersection = np.max(intersection_matrix[:, j])
            accuracy += max_intersection

        return accuracy / N

    # ------------------------------------------------------------------------------------------------------------------
    #
    # ------------------------------------------------------------------------------------------------------------------
    def save_evaluation_data(self):
        if Data.img_label.shape != Data.human_label.shape:
            QMessageBox.critical(self, "错误", "Superpixel segmentation does not match ground truth size.",
                                 QMessageBox.Yes)
            return None
        file_path, _ = FileController.save_file_dialog(self)
        if file_path:
            self.main_window.setWindowTitle('OpenCV图像超像素分割(数据计算中)')
            co = self.calculate_compactness_handle(False)
            ue = self.compute_undersegmentation_error_handle(False)
            br = self.compute_boundary_recall_action_handle(False)
            bp = self.compute_boundary_precision_handle(False)
            asa = self.compute_achievable_segmentation_accuracy_handle(False)
            self.main_window.setWindowTitle('OpenCV图像超像素分割')
            FileController.save_evaluation_data(self, file_path, co, ue, br, bp, asa)

    def open_human_segment_image(self):
        if Data.have_human_segmented_img:
            cv2.imshow("Human Segment Image", Data.human_segmented_img)

    def open_segment_image(self):
        if Data.have_segmented_img:
            cv2.imshow("Segment Image", Data.segmented_img)
