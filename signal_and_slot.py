import sys

from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QSlider, QVBoxLayout
from PySide6.QtCore import Slot, Signal, Qt


class SignalAndSlot(QWidget):
    resized = Signal(int, int)  # 发送窗口尺寸

    def __init__(self, mainwindow=None):
        super().__init__()
        self.mainwindow = mainwindow
        self.label = QLabel("初始文本", self)
        self.button = QPushButton("点击我……", self)
        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.window_size_label = QLabel()
        self.layout = QVBoxLayout(self)
        self.init_ui()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resized.emit(self.width(), self.height())

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("信号与槽")
        self.resize(800, 600)
        center = self.screen().availableGeometry().center()
        self.geometry().moveCenter(center)

        # 添加控件到布局
        layout1 = QHBoxLayout()
        layout1.addWidget(self.button)
        layout1.addWidget(self.label)
        self.layout.addLayout(layout1)

        self.slider.setRange(0, 2 ** 24 - 1)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.slider)
        self.layout.addLayout(layout2)

        layout3 = QHBoxLayout()
        self.window_size_label.setText(f'{self.size()}')
        layout3.addWidget(self.window_size_label)
        self.layout.addLayout(layout3)

        # 链接信号与槽
        self.button.clicked.connect(self.update_label)
        self.slider.valueChanged.connect(self.change_label_color)
        self.resized.connect(self.display_size)

    @Slot()
    def update_label(self):
        self.label.setText("文本已更新")

    def change_label_color(self, color):
        self.setStyleSheet(
            f"background-color: #{color:06x};"
        )
        self.label.setText(f'#{color:06x}'.upper())

    def display_size(self, w, h):
        self.window_size_label.setText(f'{w}x{h}')

    def closeEvent(self, event):
        if not self.mainwindow.isVisible():
            self.mainwindow.show()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SignalAndSlot()
    window.show()
    sys.exit(app.exec())
