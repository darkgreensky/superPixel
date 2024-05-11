import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QDockWidget
from PyQt5.QtCore import Qt

from src.attribute import Attribute
from src.evaluation import Evaluation
from src.stackedWidget import StackedWidget
from src.menuBar import MenuBar
from src.graphicsView import GraphicsView
from src.listWidgets import FuncListWidget
from src.listWidgets import UsedListWidget
from src.toolBar import ToolBar
from utils.icons import Icons
from utils.messageBox import MessageBox


class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.setObjectName("MyApp")

        # 新建对象
        self.useListWidget = UsedListWidget(self)
        self.funcListWidget = FuncListWidget(self)
        self.stackedWidget = StackedWidget(self)
        self.graphicsView = GraphicsView(self)
        self.evaluation = Evaluation(self)
        self.attribute = Attribute(self)
        self.messageBox = MessageBox(self)
        self.menu = MenuBar(self)
        self.toolBar1 = ToolBar(self)

        # 已选操作
        self.dock_used = QDockWidget(self)
        self.dock_used.setWidget(self.useListWidget)
        title_label = QLabel('已选操作')
        title_label.setObjectName('title_label')
        self.dock_used.setTitleBarWidget(title_label)
        self.dock_used.setFeatures(QDockWidget.NoDockWidgetFeatures)
        # self.dock_used.close()

        # 已选操作的属性
        self.dock_attr = QDockWidget(self)
        self.dock_attr.setWidget(self.stackedWidget)
        title_label = QLabel('属性')
        title_label.setObjectName('title_label')
        self.dock_attr.setTitleBarWidget(title_label)
        self.dock_attr.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.dock_attr.close()

        # 设置dock组件显示位置
        self.setCentralWidget(self.graphicsView)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_used)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_attr)
        self.setMenuBar(self.menu)

        self.addToolBar(self.toolBar1)
        self.toolBar1.close()

        # title and icon
        self.setWindowTitle('OpenCV图像超像素分割')
        icon = Icons.create_svg_icon(Icons.grape)
        self.setWindowIcon(icon)

        self.resize(950, 600)

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
    app.setStyleSheet(open('./utils/styleSheet.qss', encoding='utf-8').read())
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
