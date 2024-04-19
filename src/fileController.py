import cv2
import numpy as np
from PyQt5.QtWidgets import QFileDialog

from src.listWidgetItems import MyItem


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
                    print("Error: Failed to load image")
            else:
                print("Error: Unsupported file format")
        return None

    @staticmethod
    def save_label(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "保存文件", "", "seg files (*.seg);;All files (*)")
        if file_path:
            with open(file_path, 'w') as f:
                for row in MyItem.img_label:
                    line = ' '.join(map(str, row))  # 将每行数据转换为字符串，并用空格连接
                    f.write("%s\n" % line)
            print("数据已保存到文件:", file_path)

    @staticmethod
    def open_seg_label_of_human(parent):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(parent, "Open File", "", "Segments Files (*.seg)",
                                                   options=options)
        if file_name:
            print("Selected file:", file_name)
            if file_name.endswith('.seg'):
                return FileController.read_segments_label_file(file_name)
            else:
                print("Error: Unsupported file format")
        return None, None


    @staticmethod
    def read_segments_label_file(file_name):
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
        segment_label = [[0 for i in range(width)] for i in range(height)]
        for line in lines[i:]:
            s, y, x1, x2 = map(int, line.split())
            for j in range(x1, x2 + 1):
                segment_label[y][j] = s
        return segment_label, num_segments
