import cv2
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QCursor, QImage, QPixmap, QColor
from PyQt5.QtWidgets import QGraphicsView, QGraphicsPixmapItem, QGraphicsScene, QMenu, QAction, QFileDialog


class GraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent=parent)
        self.setObjectName('GraphicsView')
        self._zoom = 0
        self._empty = True
        self._photo = QGraphicsPixmapItem()
        self._scene = QGraphicsScene(self)
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setAlignment(Qt.AlignCenter)  # 居中显示
        self.setDragMode(QGraphicsView.ScrollHandDrag)  # 设置拖动
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMinimumSize(640, 512)

    def contextMenuEvent(self, event):
        if not self.has_photo():
            return
        menu = QMenu()
        save_action = QAction('另存为', self)
        save_action.triggered.connect(self.save_current)  # 传递额外值
        menu.addAction(save_action)
        menu.exec(QCursor.pos())

    def save_current(self):
        file_name = QFileDialog.getSaveFileName(self, '另存为', './', 'Image files(*.png *.gif *.jpg)')[0]
        if file_name:
            self._photo.pixmap().save(file_name)

    def get_image(self):
        if self.has_photo():
            return self._photo.pixmap().toImage()

    def has_photo(self):
        return not self._empty

    def change_image(self, img):
        self.update_image(img)
        self.fitInView()

    @staticmethod
    def img_to_pixmap(img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # bgr -> rgb
        h, w, c = img.shape  # 获取图片形状
        image = QImage(img, w, h, 3 * w, QImage.Format_RGB888)
        return QPixmap.fromImage(image)

    def update_image(self, img):
        self._empty = False
        self._photo.setPixmap(self.img_to_pixmap(img))

    def fitInView(self, *args, **kwargs):
        rect = QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.has_photo():
                unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                view_rect = self.viewport().rect()
                scene_rect = self.transform().mapRect(rect)
                factor = min(view_rect.width() / scene_rect.width(),
                             view_rect.height() / scene_rect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def wheelEvent(self, event):
        if self.has_photo():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom >= -10:
                if self._zoom == 0:
                    self.fitInView()
                else:
                    self.scale(factor, factor)
            else:
                self._zoom = -10