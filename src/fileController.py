# src/fileController.py
import cv2
import numpy as np
from PyQt5.QtWidgets import QFileDialog


class FileController:
    def __init__(self, parent=None):
        self.mainwindow = parent

    def open_file_dialog(self, parent):
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
