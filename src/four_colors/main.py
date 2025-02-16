from collections import defaultdict
import sys
from typing import Optional

from PySide6.QtGui import QColor, QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGraphicsPixmapItem,
    QGraphicsScene,
    QMainWindow,
    QPushButton,
)

from .view import CostumGraphicsView
from .view.ui_compiled.main import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)


class App:
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        self.graphicsView = CostumGraphicsView()
        self.window.c_image_main.layout().addWidget(self.graphicsView)
        self.window.actionLoad.triggered.connect(self._cb_lead_image_button)

        self.image: Optional[QImage] = None

        return
        colors = self.extract_prominent_colors(file_path)
        for c in colors:
            b = QPushButton()
            b.setStyleSheet(f"background-color: rgb({c[0]}, {c[1]}, {c[2]});")
            self.window.c_colors.addWidget(b)

    def run(self) -> QApplication:
        self.window.show()
        sys.exit(self.app.exec())

    def quit(self):
        self.app.quit()

    def get_image_path(self) -> str:
        file_name, _ = QFileDialog.getOpenFileName(
            None,
            "Open Image File",
            "",
            "Images (*.png *.xpm *.jpg *.jpeg *.bmp *.gif *.webp)",  # Add more image formats if needed
        )
        return file_name

    def load_image(self):
        file_path = self.get_image_path()
        image = QImage(file_path)
        if image.format() != QImage.Format.Format_RGB888:
            image = image.convertToFormat(QImage.Format.Format_RGB888)
        self.image = image

    def extract_prominent_colors(self, file_path):
        if not self.image:
            return
        le_colors = defaultdict(int)
        for y in range(self.image.height()):
            for x in range(self.image.width()):
                color = QColor(self.image.pixel(x, y))
                color_tuple = color.getRgb()[:3]
                le_colors[color_tuple] += 1

        i = 0
        colors_return = []
        for t, _ in sorted(le_colors.items(), key=lambda x: x[1], reverse=True):
            i += 1
            colors_return.append(t)
            if i == 4:
                break
        return colors_return

    def _cb_lead_image_button(self):
        self.load_image()
        if not self.image:
            return
        self.graphicsView.display_image(self.image)
