from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QGridLayout


class MessageBox(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent

        self.label = QLabel()
        self.label.setStyleSheet("font-size: 20px;")
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label.setCursor(Qt.IBeamCursor)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QGridLayout(self.centralWidget)
        self.layout.setVerticalSpacing(1)  # 设置垂直间距
        self.layout.setContentsMargins(10, 30, 10, 30)
        self.layout.addWidget(self.label)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinimizeButtonHint)
        self.setFixedWidth(250)
        self.setFixedHeight(110)

    def get_message(self, message: str, title="提示"):
        self.setWindowTitle(title)
        self.label.setText(message)
        self.show()
