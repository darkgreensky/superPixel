import cv2
import numpy as np
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from utils.data import Data


class FileController:
    def __init__(self, parent=None):
        self.main_window = parent

    @staticmethod
    def open_file_dialog(parent):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(parent, "Open File", "", "All Files (*);;Text Files (*.txt)",
                                                   options=options)
        if file_name:
            print("Selected file:", file_name)
            if file_name.endswith(('.jpg', '.png', '.bmp', '.jpeg')):
                src_img = cv2.imdecode(np.fromfile(file_name, dtype=np.uint8), -1)
                if src_img is not None:
                    return src_img
                else:
                    QMessageBox.critical(parent, "Error", "Failed to load image")
            else:
                QMessageBox.critical(parent, "Error", "Unsupported file format")
        return None

    @staticmethod
    def save_label(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "保存文件", "", "seg files (*.mseg);;All files (*)")
        if file_path:
            with open(file_path, 'w') as f:
                label = Data.img_label
                if self.main_window.cur_img is not None:
                    height, width = self.main_window.cur_img.shape[:2]
                    f.write("height %d\n" % height)
                    f.write("width %d\n" % width)
                if len(label) != 0:
                    self.main_window.attribute.get_image_info()
                    f.write("segments %d\n" % self.main_window.attribute.num_superpixels)
                    count = 0
                    num = label[0][0]
                    f.write("label_idx count\n")
                    for i in range(height):
                        for j in range(width):
                            if label[i][j] == num:
                                count += 1
                            else:
                                f.write("%d %d\n" % (num, count))
                                count = 1
                                num = label[i][j]
                    if count != 0:
                        f.write("%d %d" % (num, count))
                else:
                    QMessageBox.information(self, "提示", "未进行过超像素分割，保存失败！",
                                            QMessageBox.Yes)
            QMessageBox.information(self, "提示", "数据已保存到文件:{}".format(file_path),
                                    QMessageBox.Yes)

    @staticmethod
    def open_seg_label_of_algorithm(parent):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(parent, "Open File", "", "Segments Files (*.mseg)",
                                                   options=options)
        if file_name:
            print("Selected file:", file_name)
            if file_name.endswith('.mseg'):
                return FileController.read_algorithm_segments_label_file(file_name)
            else:
                QMessageBox.critical(parent, "Error", "Unsupported file format")
        return None, None, None

    @staticmethod
    def read_algorithm_segments_label_file(file_name):
        print(file_name)
        with open(file_name, "r") as f:
            lines = f.readlines()
        height = int(lines[0].split()[1])
        width = int(lines[1].split()[1])
        num_segments = int(lines[2].split()[1])

        segmented_img = np.zeros((height, width, 3), dtype=np.uint8)
        labels = np.zeros((height, width), dtype=np.uint16)

        # 设置区域颜色
        colors = np.random.randint(0, 255, size=(num_segments, 3), dtype=np.uint8)

        # 填充图像
        idx = 4
        num, count = map(int, lines[idx].split())
        idx += 1
        for i in range(height):
            for j in range(width):
                if count:
                    segmented_img[i, j] = colors[num]
                    labels[i, j] = num
                    count -= 1
                else:
                    num, count = map(int, lines[idx].split())
                    idx += 1
                    segmented_img[i, j] = colors[num]
                    labels[i, j] = num
                    count -= 1
        return labels, num_segments, segmented_img


    @staticmethod
    def open_seg_label_of_human(parent):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(parent, "Open File", "", "Segments Files (*.seg)",
                                                   options=options)
        if file_name:
            print("Selected file:", file_name)
            if file_name.endswith('.seg'):
                return FileController.read_human_segments_label_file(file_name)
            else:
                QMessageBox.critical(parent, "Error", "Unsupported file format")
        return None, None, None


    @staticmethod
    def read_human_segments_label_file(file_name):
        print(file_name)
        with open(file_name, "r") as f:
            lines = f.readlines()
        width = 0
        height = 0
        num_segments = 0
        i = 0
        while True:
            if lines[i].split()[0] == 'width':
                width = int(lines[i].split()[1])
            elif lines[i].split()[0] == 'height':
                height = int(lines[i].split()[1])
            elif lines[i].split()[0] == 'segments':
                num_segments = int(lines[i].split()[1])
            elif lines[i].split()[0] == 'data':
                i += 1
                break
            i += 1

        segmented_img = np.zeros((height, width, 3), dtype=np.uint8)
        true_labels = np.zeros((height, width), dtype=np.uint16)

        # 设置区域颜色
        colors = np.random.randint(0, 255, size=(num_segments, 3), dtype=np.uint8)

        # 填充图像
        for line in lines[11:]:
            s, y, x1, x2 = map(int, line.split())
            segmented_img[y, x1: x2] = colors[s]
            true_labels[y, x1: x2] = s
        return true_labels, num_segments, segmented_img

    @staticmethod
    def save_evaluation_data(parent, co, ue, rec, asa):
        file_path, _ = QFileDialog.getSaveFileName(parent, "保存文件", "", "txt files (*.txt);;All files (*)")
        if file_path:
            with open(file_path, 'w') as f:
                f.write("紧凑度\t\t{}\n".format(co))
                f.write("欠分割误差\t{}\n".format(ue))
                f.write("边界召回率\t{}\n".format(rec))
                f.write("可达分割精度\t{}\n".format(asa))
        QMessageBox.information(parent, "提示", "数据已保存到文件:{}".format(file_path),
                                QMessageBox.Ok)