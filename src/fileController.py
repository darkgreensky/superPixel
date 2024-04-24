import datetime
import cv2
import numpy as np
import openpyxl
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from src.attribute import Attribute
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
                    height, width = src_img.shape[:2]
                    Data.update_img_info(height=height, width=width, num_superpixels=0, use_algorithm='')
                    return src_img
                else:
                    QMessageBox.critical(parent, "Error", "Failed to load image")
            else:
                QMessageBox.critical(parent, "Error", "Unsupported file format")
        return None

    @staticmethod
    def save_label(self):
        label = Data.img_label
        if self.main_window.cur_img is not None and len(label) != 0:
            if Data.img_type:
                QMessageBox.information(self, "提示", "打开过数据分割文件,请重新计算超像素数据后保存。",
                                        QMessageBox.Ok)
            else:
                file_path, _ = QFileDialog.getSaveFileName(self, "保存文件", "", "seg files (*.mseg);;All files (*)")
                if file_path:
                    with open(file_path, 'w') as f:
                        if self.main_window.cur_img is not None:
                            height, width = self.main_window.cur_img.shape[:2]
                            current_time = datetime.datetime.now()
                            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
                            f.write("date %s\n" % formatted_time)
                            f.write("height %d\n" % height)
                            f.write("width %d\n" % width)
                        else:
                            QMessageBox.critical(self, "错误", "没有图像！")
                        if len(label) != 0:
                            Attribute.update_num_superpixels()
                            f.write("algorithm %s\n" % Data.use_algorithm)
                            f.write("segments %d\n" % Data.num_superpixels)
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
                            QMessageBox.critical(self, "错误", "没有超像素分割信息!")
                    QMessageBox.information(self, "提示", "数据已保存到文件: {}".format(file_path),
                                            QMessageBox.Ok)
                else:
                    QMessageBox.critical(self, "错误", "路径错误!")
        else:
            QMessageBox.information(self, "提示", "未进行过超像素分割，保存失败！",
                                    QMessageBox.Ok)

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
        return None, None, None, None, None, None

    @staticmethod
    def read_algorithm_segments_label_file(file_name):
        print(file_name)
        with open(file_name, "r") as f:
            lines = f.readlines()
        height = int(lines[1].split()[1])
        width = int(lines[2].split()[1])
        use_algorithm = str(lines[3].split()[1])
        num_segments = int(lines[4].split()[1])

        segmented_img = np.zeros((height, width, 3), dtype=np.uint8)
        labels = np.zeros((height, width), dtype=np.uint16)

        # 设置区域颜色
        colors = np.random.randint(0, 255, size=(num_segments, 3), dtype=np.uint8)

        # 填充图像
        idx = 6
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
        return labels, num_segments, segmented_img, height, width, use_algorithm

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
    def save_evaluation_data(parent, file_path, co, ue, br, bp, asa):
        if file_path:
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet["A1"] = "超像素数目"
            sheet["B1"] = Data.num_superpixels
            sheet["A2"] = "分割算法"
            sheet["B2"] = Data.use_algorithm
            sheet["A3"] = "紧凑度"
            sheet["B3"] = float("{:.6f}".format(co))
            sheet["A4"] = "欠分割误差"
            sheet["B4"] = float("{:.6f}".format(ue))
            sheet["A5"] = "边界召回率"
            sheet["B5"] = float("{:.6f}".format(br))
            sheet["A6"] = "边界精度"
            sheet["B6"] = float("{:.6f}".format(bp))
            sheet["A7"] = "可达分割精度"
            sheet["B7"] = float("{:.6f}".format(asa))
            workbook.save(file_path)

            # with open(file_path, 'w') as f:
            #     f.write("超像素数目\t{}\n".format(Data.num_superpixels))
            #     f.write("分割算法\t\t{}\n".format(Data.use_algorithm))
            #     f.write("紧凑度\t\t{:.6f}\n".format(co))
            #     f.write("欠分割误差\t{:.6f}\n".format(ue))
            #     f.write("边界召回率\t{:.6f}\n".format(br))
            #     f.write("边界精度\t\t{:.6f}\n".format(bp))
            #     f.write("可达分割精度\t{:.6f}\n".format(asa))
            QMessageBox.information(parent, "提示", "数据已保存到文件: {}".format(file_path),
                                    QMessageBox.Ok)

    @staticmethod
    def save_file_dialog(parent):
        file_path, _ = QFileDialog.getSaveFileName(parent, "保存文件", "", "xlsx files (*.xlsx);;All files (*)")
        if file_path:
            return file_path, _
        return None, None
