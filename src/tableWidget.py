from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class TableWidget(QTableWidget):
    def __init__(self, parent=None):
        super(TableWidget, self).__init__(parent=parent)
        self.mainwindow = parent
        self.setShowGrid(True)  # 显示网格
        self.setAlternatingRowColors(True)  # 隔行显示颜色
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().sectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().sectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setStretchLastSection(True)
        self.setFocusPolicy(Qt.NoFocus)

    def update_item(self):
        param = self.get_params()
        self.mainwindow.useListWidget.currentItem().update_params(param)
        self.mainwindow.update_image()

    def update_params(self, param=None):
        for key in param.keys():
            box = self.findChild(QWidget, name=key)
            if isinstance(box, QSpinBox) or isinstance(box, QDoubleSpinBox):
                box.setValue(param[key])
            elif isinstance(box, QComboBox):
                box.setCurrentIndex(param[key])
            elif isinstance(box, QCheckBox):
                box.setChecked(param[key])

    def get_params(self):
        param = {}
        for spinbox in self.findChildren(QSpinBox):
            param[spinbox.objectName()] = spinbox.value()
        for doublespinbox in self.findChildren(QDoubleSpinBox):
            param[doublespinbox.objectName()] = doublespinbox.value()
        for combox in self.findChildren(QComboBox):
            param[combox.objectName()] = combox.currentIndex()
        for combox in self.findChildren(QCheckBox):
            param[combox.objectName()] = combox.isChecked()
        for slider in self.findChildren(QSlider):
            param[slider.objectName()] = slider.value()
        return param


class GrayingTableWidget(TableWidget):
    def __init__(self, parent=None):
        super(GrayingTableWidget, self).__init__(parent=parent)


class EdgeTableWidget(TableWidget):
    def __init__(self, parent=None):
        super(EdgeTableWidget, self).__init__(parent=parent)

        self.thresh1_spinBox = QSpinBox()
        self.thresh1_spinBox.setMinimum(0)
        self.thresh1_spinBox.setMaximum(255)
        self.thresh1_spinBox.setSingleStep(1)
        self.thresh1_spinBox.setObjectName('thresh1')
        self.thresh1_spinBox.valueChanged.connect(self.update_item)

        self.thresh2_spinBox = QSpinBox()
        self.thresh2_spinBox.setMinimum(0)
        self.thresh2_spinBox.setMaximum(255)
        self.thresh2_spinBox.setSingleStep(1)
        self.thresh2_spinBox.setObjectName('thresh2')
        self.thresh2_spinBox.valueChanged.connect(self.update_item)

        self.setColumnCount(2)
        self.setRowCount(2)

        self.setItem(0, 0, QTableWidgetItem('阈值1'))
        self.setCellWidget(0, 1, self.thresh1_spinBox)
        self.setItem(1, 0, QTableWidgetItem('阈值2'))
        self.setCellWidget(1, 1, self.thresh2_spinBox)


class GammaITabelWidget(TableWidget):
    def __init__(self, parent=None):
        super(GammaITabelWidget, self).__init__(parent=parent)
        self.gamma_slider = QSlider()
        self.gamma_slider.setOrientation(Qt.Horizontal)
        self.gamma_slider.setMinimum(0)
        self.gamma_slider.setMaximum(300)  # 设置最大值，这个值可以根据您的需要进行调整
        self.gamma_slider.setSingleStep(1)
        self.gamma_slider.setValue(100)
        self.gamma_slider.setObjectName('gamma')

        self.gamma_lineedit = QLineEdit('1.0')
        self.gamma_lineedit.setValidator(QDoubleValidator())  # 设置验证器，只允许输入浮点数3
        self.gamma_lineedit.setFixedWidth(50)  # 设置输入框的宽度

        self.setColumnCount(2)
        self.setRowCount(1)

        self.setItem(0, 0, QTableWidgetItem('gamma'))

        layout = QHBoxLayout()
        layout.addWidget(self.gamma_slider)
        layout.addWidget(self.gamma_lineedit)
        layout.setContentsMargins(0, 0, 0, 0)

        widget = QWidget()
        widget.setLayout(layout)

        self.gamma_slider.valueChanged.connect(self.update_item)
        self.gamma_slider.valueChanged.connect(self.update_lineedit)
        self.gamma_lineedit.editingFinished.connect(self.update_slider)

        self.setCellWidget(0, 1, widget)

    def update_lineedit(self):
        value = self.gamma_slider.value() / 100.0  # 根据需要进行调整
        self.gamma_lineedit.setText(str(value))

    def update_slider(self):
        text = self.gamma_lineedit.text()
        if text:
            value = float(text)
            self.gamma_slider.setValue(int(value * 100))  # 根据需要进行调整


class SkimageSLICTableWidget(TableWidget):
    def __init__(self, parent=None):
        super(SkimageSLICTableWidget, self).__init__(parent=parent)
        self.num_segments_spinBox = QSpinBox()
        self.num_segments_spinBox.setMinimum(0)
        self.num_segments_spinBox.setMaximum(10000)
        self.num_segments_spinBox.setSingleStep(1)
        self.num_segments_spinBox.setObjectName('num_segments')

        self.compactness_spinBox = QSpinBox()
        self.compactness_spinBox.setMinimum(1)
        self.compactness_spinBox.setMaximum(255)
        self.compactness_spinBox.setSingleStep(1)
        self.compactness_spinBox.setObjectName('compactness')

        self.sigma_spinBox = QSpinBox()
        self.sigma_spinBox.setMinimum(0)
        self.sigma_spinBox.setMaximum(255)
        self.sigma_spinBox.setSingleStep(1)
        self.sigma_spinBox.setObjectName('sigma')

        self.setColumnCount(2)
        self.setRowCount(4)

        self.setItem(0, 0, QTableWidgetItem('超像素数目'))
        self.setCellWidget(0, 1, self.num_segments_spinBox)
        self.setItem(1, 0, QTableWidgetItem('紧凑度'))
        self.setCellWidget(1, 1, self.compactness_spinBox)
        self.setItem(2, 0, QTableWidgetItem('高斯平滑标准差'))
        self.setCellWidget(2, 1, self.sigma_spinBox)
        self.setSpan(3, 0, 1, 2)

        self.start_Button = QPushButton('确定')
        self.start_Button.clicked.connect(self.button_click)
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.start_Button)
        self.buttonWidget = QWidget()
        self.buttonWidget.setLayout(self.buttonLayout)

        self.verticalHeader().resizeSection(3, 60)

        self.setCellWidget(3, 0, self.buttonWidget)  # 设置按钮 Widget 在单元格中水平和垂直居中

    def button_click(self):
        self.update_item()


class OpenCVSLICTableWidget(TableWidget):
    def __init__(self, parent=None):
        super(OpenCVSLICTableWidget, self).__init__(parent=parent)
        self.algorithm_box = QComboBox()
        self.algorithm_box.addItem("SLIC")
        self.algorithm_box.addItem("SLICO")
        self.algorithm_box.addItem("MSLIC")
        self.algorithm_box.setObjectName('algorithm')

        # 平均超像素大小
        self.region_size_spinBox = QSpinBox()
        self.region_size_spinBox.setMinimum(1)
        self.region_size_spinBox.setMaximum(500)
        self.region_size_spinBox.setSingleStep(1)
        self.region_size_spinBox.setObjectName('region_size')

        # 超像素平滑度
        self.ruler_spinBox = QSpinBox()
        self.ruler_spinBox.setMinimum(0)
        self.ruler_spinBox.setMaximum(50)
        self.ruler_spinBox.setSingleStep(1)
        self.ruler_spinBox.setObjectName('ruler')

        # 迭代次数  iterate_times
        self.iterateTimes_spinBox = QSpinBox()
        self.iterateTimes_spinBox.setMinimum(0)
        self.iterateTimes_spinBox.setMaximum(100)
        self.iterateTimes_spinBox.setSingleStep(1)
        self.iterateTimes_spinBox.setObjectName('iterate_times')

        self.checkbox_layout = QHBoxLayout()
        # 是否显示边界
        self._edge_checkBox = QCheckBox()
        self.checkbox1 = QCheckBox('显示边界')
        self.checkbox_layout.addWidget(self.checkbox1)
        self.checkboxWidget = QWidget()
        self.checkbox1.setObjectName('edge')

        # 是否色彩填充
        self._color_checkBox = QCheckBox()
        self.checkbox2 = QCheckBox('色彩填充')
        self.checkbox_layout.addWidget(self.checkbox2)
        self.checkboxWidget = QWidget()
        self.checkbox2.setObjectName('color_fill')

        self.checkboxWidget.setLayout(self.checkbox_layout)
        self.setColumnCount(2)
        self.setRowCount(6)

        self.setItem(0, 0, QTableWidgetItem('算法选择'))
        self.setCellWidget(0, 1, self.algorithm_box)
        self.setItem(1, 0, QTableWidgetItem('平均超像素大小'))
        self.setCellWidget(1, 1, self.region_size_spinBox)
        self.setItem(2, 0, QTableWidgetItem('超像素平滑度'))
        self.setCellWidget(2, 1, self.ruler_spinBox)
        self.setItem(3, 0, QTableWidgetItem('迭代次数'))
        self.setCellWidget(3, 1, self.iterateTimes_spinBox)

        self.setSpan(4, 0, 1, 2)
        self.setSpan(5, 0, 1, 2)

        self.start_Button = QPushButton('确定')
        self.start_Button.clicked.connect(self.button_click)
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.start_Button)
        self.buttonWidget = QWidget()
        self.buttonWidget.setLayout(self.buttonLayout)

        self.verticalHeader().resizeSection(4, 50)
        self.verticalHeader().resizeSection(5, 60)

        self.setCellWidget(4, 0, self.checkboxWidget)
        self.setCellWidget(5, 0, self.buttonWidget)  # 设置按钮 Widget 在单元格中水平和垂直居中

    def button_click(self):
        self.update_item()


class OpenCVSEEDSTableWidget(TableWidget):
    def __init__(self, parent=None):
        super(OpenCVSEEDSTableWidget, self).__init__(parent=parent)
        # 超像素数目
        self.num_superpixels_spinBox = QSpinBox()
        self.num_superpixels_spinBox.setMinimum(1)
        self.num_superpixels_spinBox.setMaximum(10000)
        self.num_superpixels_spinBox.setSingleStep(1)
        self.num_superpixels_spinBox.setObjectName('num_superpixels')

        # 块级别数
        self.num_levels_spinBox = QSpinBox()
        self.num_levels_spinBox.setMinimum(0)
        self.num_levels_spinBox.setMaximum(50)
        self.num_levels_spinBox.setSingleStep(1)
        self.num_levels_spinBox.setObjectName('num_levels')

        # 迭代次数  iterate_times
        self.iterateTimes_spinBox = QSpinBox()
        self.iterateTimes_spinBox.setMinimum(0)
        self.iterateTimes_spinBox.setMaximum(100)
        self.iterateTimes_spinBox.setSingleStep(1)
        self.iterateTimes_spinBox.setObjectName('iterate_times')

        self.checkbox_layout = QHBoxLayout()
        # 是否显示边界
        self._edge_checkBox = QCheckBox()
        self.checkbox1 = QCheckBox('显示边界')
        self.checkbox_layout.addWidget(self.checkbox1)
        self.checkboxWidget = QWidget()
        self.checkbox1.setObjectName('edge')

        # 是否色彩填充
        self._color_checkBox = QCheckBox()
        self.checkbox2 = QCheckBox('色彩填充')
        self.checkbox_layout.addWidget(self.checkbox2)
        self.checkboxWidget = QWidget()
        self.checkbox2.setObjectName('color_fill')

        self.checkboxWidget.setLayout(self.checkbox_layout)
        self.setColumnCount(2)
        self.setRowCount(5)

        self.setItem(0, 0, QTableWidgetItem('超像素数目'))
        self.setCellWidget(0, 1, self.num_superpixels_spinBox)
        self.setItem(1, 0, QTableWidgetItem('块级别数'))
        self.setCellWidget(1, 1, self.num_levels_spinBox)
        self.setItem(2, 0, QTableWidgetItem('迭代次数'))
        self.setCellWidget(2, 1, self.iterateTimes_spinBox)

        self.setSpan(3, 0, 1, 2)
        self.setSpan(4, 0, 1, 2)

        self.start_Button = QPushButton('确定')
        self.start_Button.clicked.connect(self.button_click)
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.start_Button)
        self.buttonWidget = QWidget()
        self.buttonWidget.setLayout(self.buttonLayout)

        self.verticalHeader().resizeSection(3, 50)
        self.verticalHeader().resizeSection(4, 60)

        self.setCellWidget(3, 0, self.checkboxWidget)
        self.setCellWidget(4, 0, self.buttonWidget)  # 设置按钮 Widget 在单元格中水平和垂直居中

    def button_click(self):
        self.update_item()


class OpenCVLSCTableWidget(TableWidget):
    def __init__(self, parent=None):
        super(OpenCVLSCTableWidget, self).__init__(parent=parent)
        # 平均超像素大小
        self.num_superpixels_spinBox = QSpinBox()
        self.num_superpixels_spinBox.setMinimum(1)
        self.num_superpixels_spinBox.setMaximum(500)
        self.num_superpixels_spinBox.setSingleStep(1)
        self.num_superpixels_spinBox.setObjectName('region_size')

        # 紧凑度因子
        self.num_levels_slider = QSlider()
        self.num_levels_slider.setOrientation(Qt.Horizontal)
        self.num_levels_slider.setMinimum(0)
        self.num_levels_slider.setMaximum(1000)
        self.num_levels_slider.setSingleStep(1)
        self.num_levels_slider.setValue(75)
        self.num_levels_slider.setObjectName('ratio')
        self.num_levels_lineedit = QLineEdit('0.075')
        self.num_levels_lineedit.setValidator(QDoubleValidator())
        self.num_levels_lineedit.setFixedWidth(50)
        self.setColumnCount(2)
        self.setRowCount(1)
        self.setItem(0, 0, QTableWidgetItem('ratio'))
        layout = QHBoxLayout()
        layout.addWidget(self.num_levels_slider)
        layout.addWidget(self.num_levels_lineedit)
        layout.setContentsMargins(0, 0, 0, 0)
        num_levels_widget = QWidget()
        num_levels_widget.setLayout(layout)
        self.num_levels_slider.valueChanged.connect(self.update_lineedit)
        self.num_levels_lineedit.editingFinished.connect(self.update_slider)

        # 迭代次数
        self.iterateTimes_spinBox = QSpinBox()
        self.iterateTimes_spinBox.setMinimum(0)
        self.iterateTimes_spinBox.setMaximum(100)
        self.iterateTimes_spinBox.setSingleStep(1)
        self.iterateTimes_spinBox.setObjectName('iterate_times')

        self.checkbox_layout = QHBoxLayout()
        # 是否显示边界
        self._edge_checkBox = QCheckBox()
        self.checkbox1 = QCheckBox('显示边界')
        self.checkbox_layout.addWidget(self.checkbox1)
        self.checkboxWidget = QWidget()
        self.checkbox1.setObjectName('edge')

        # 是否色彩填充
        self._color_checkBox = QCheckBox()
        self.checkbox2 = QCheckBox('色彩填充')
        self.checkbox_layout.addWidget(self.checkbox2)
        self.checkboxWidget = QWidget()
        self.checkbox2.setObjectName('color_fill')

        self.checkboxWidget.setLayout(self.checkbox_layout)
        self.setColumnCount(2)
        self.setRowCount(5)

        self.setItem(0, 0, QTableWidgetItem('平均超像素大小'))
        self.setCellWidget(0, 1, self.num_superpixels_spinBox)
        self.setItem(1, 0, QTableWidgetItem('紧凑度因子'))
        self.setCellWidget(1, 1, num_levels_widget)
        self.setItem(2, 0, QTableWidgetItem('迭代次数'))
        self.setCellWidget(2, 1, self.iterateTimes_spinBox)

        self.setSpan(3, 0, 1, 2)
        self.setSpan(4, 0, 1, 2)

        self.start_Button = QPushButton('确定')
        self.start_Button.clicked.connect(self.button_click)
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.start_Button)
        self.buttonWidget = QWidget()
        self.buttonWidget.setLayout(self.buttonLayout)

        self.verticalHeader().resizeSection(3, 50)
        self.verticalHeader().resizeSection(4, 60)

        self.setCellWidget(3, 0, self.checkboxWidget)
        self.setCellWidget(4, 0, self.buttonWidget)  # 设置按钮 Widget 在单元格中水平和垂直居中

    def button_click(self):
        self.update_item()

    def update_lineedit(self):
        value = self.num_levels_slider.value() / 1000.0  # 根据需要进行调整
        self.num_levels_lineedit.setText(str(value))

    def update_slider(self):
        text = self.num_levels_lineedit.text()
        if text:
            value = float(text)
            self.num_levels_slider.setValue(int(value * 1000))  # 根据需要进行调整
