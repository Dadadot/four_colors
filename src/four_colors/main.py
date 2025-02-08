from collections import defaultdict
import sys

from PySide6.QtGui import QColor, QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QGraphicsPixmapItem,
    QGraphicsScene,
    QMainWindow,
    QPushButton,
)

from .view.ui_compiled.main import Ui_MainWindow
from .model import ImageLoader


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)


class App:
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        self.image_loader = ImageLoader()
        self.graphic_scene = QGraphicsScene()
        self.window.graphicsView.setScene(self.graphic_scene)
        self.window.pushButton.clicked.connect(lambda: self.load_image())

    def run(self) -> QApplication:
        self.window.show()
        sys.exit(self.app.exec())

    def quit(self):
        self.app.quit()

    def load_image(self):
        file_path = self.image_loader.get_image_path()
        pixmap_item = self.image_loader.get_pixmap_item(file_path)
        self.graphic_scene.addItem(pixmap_item)
        colors = self.extract_prominent_colors(file_path)
        for c in colors:
            b = QPushButton()
            b.setStyleSheet(f"background-color: rgb({c[0]}, {c[1]}, {c[2]});")
            self.window.c_colors.addWidget(b)


    def extract_prominent_colors(self, file_path):
        le_colors = defaultdict(int)
        image = QImage(file_path)
        if image.format() != QImage.Format.Format_RGB888:
            image = image.convertToFormat(QImage.Format.Format_RGB888)

        for y in range(image.height()):
            for x in range(image.width()):
                color = QColor(image.pixel(x, y))
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
