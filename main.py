import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from src.stackedWidget import StackedWidget
from src.menuBar import MenuBar
from src.graphicsView import GraphicsView
from src.listWidgets import FuncListWidget
from src.listWidgets import UsedListWidget
from utils.icons import Icons



class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()

        self.useListWidget = UsedListWidget(self)
        self.funcListWidget = FuncListWidget(self)
        self.stackedWidget = StackedWidget(self)
        self.graphicsView = GraphicsView(self)
        self.icons = Icons()

        self.dock_used = QDockWidget(self)
        self.dock_used.setWidget(self.useListWidget)
        self.dock_used.setTitleBarWidget(QLabel('已选操作'))
        self.dock_used.setFeatures(QDockWidget.NoDockWidgetFeatures)

        self.dock_attr = QDockWidget(self)
        self.dock_attr.setWidget(self.stackedWidget)
        self.dock_attr.setTitleBarWidget(QLabel('属性'))
        self.dock_attr.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.dock_attr.close()

        self.setCentralWidget(self.graphicsView)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_used)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_attr)

        self.menu = MenuBar(self)
        self.setMenuBar(self.menu)

        self.setWindowTitle('Opencv图像处理')
        icon = self.icons.create_svg_icon(self.icons.grape)
        self.setWindowIcon(icon)
        # self.setWindowIcon(QIcon('resources/icons/main.png'))
        self.src_img = None
        self.cur_img = None

    def update_image(self):
        if self.src_img is None:
            return
        img = self.process_image()
        self.cur_img = img
        self.graphicsView.update_image(img)

    def change_image(self, img):
        self.src_img = img
        img = self.process_image()
        self.cur_img = img
        self.graphicsView.change_image(img)

    def process_image(self):
        img = self.src_img.copy()
        for i in range(self.useListWidget.count()):
            img = self.useListWidget.item(i)(img)
        return img


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
