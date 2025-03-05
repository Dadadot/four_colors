from collections import defaultdict
import sys
from typing import Optional

from PySide6.QtCore import QRectF
from PySide6.QtGui import QColor, QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QPushButton,
    QGraphicsView,
)

from .view import CostumGraphicsView, SelectionGraphicsView, WidgetColor
from .view.ui_compiled.main import Ui_MainWindow
from . import Signals, color_names


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)


class App:
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        self.graphicsView = SelectionGraphicsView()
        self.selection_graphicsView = CostumGraphicsView()
        self.window.c_image_main.layout().addWidget(self.graphicsView)
        self.window.c_image_selection.layout().addWidget(self.selection_graphicsView)
        self.window.actionLoad.triggered.connect(self._cb_lead_image_button)
        self.image: Optional[QImage] = None
        Signals.RectangleSelected.connect(self._on_rectangel_selected)
        self.color_widgets = []
        for i in range(4):
            x = WidgetColor("No Name", (0, 0, 0))
            self.window.c_colors.layout().addWidget(x)
            self.color_widgets.append(x)

        return
        colors = self.extract_colors(file_path)
        for c in colors:
            b = QPushButton()
            b.setStyleSheet(f"background-color: rgb({c[0]}, {c[1]}, {c[2]});")
            self.window.c_colors.addWidget(b)

    def _on_rectangel_selected(self, rect: QRectF):
        if not self.image:
            return
        x = self.image.copy(rect.toRect())
        self.selection_graphicsView.display_image(x)
        colors = self.extract_colors(x)
        named_colors = self.get_named_colors(colors)
        self._update_c_colors(named_colors)

    def _update_c_colors(self, colors):
        for i, item in enumerate(colors):
            if i == 4:
                break
            rgb, name = item
            w = self.color_widgets[i]
            w.set_color(name, rgb)

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

    def extract_colors(self, image: QImage):
        le_colors = defaultdict(int)
        for y in range(image.height()):
            for x in range(image.width()):
                color = QColor(image.pixel(x, y))
                color_tuple = color.getRgb()[:3]
                le_colors[color_tuple] += 1
        le_colors_sorted = sorted(le_colors.items(), key=lambda x: x[1], reverse=True)
        le_colors_sorted = [color for color, count in le_colors_sorted]
        return le_colors_sorted

    def get_named_colors(self, colors):
        named_color_count = defaultdict(int)
        for color in colors:
            distances = []
            r1, g1, b1 = color
            for k, v in color_names.items():
                r2, g2, b2 = k
                distance = abs(r1 - r2) + abs(g1 - g2) + abs(b1 - b2)
                distances.append(distance)
            color_distance_zip = list(zip(color_names.keys(), distances))
            color_distance_zip.sort(key=lambda x: x[1])
            tmp_color = color_distance_zip[0][0]
            distance = color_distance_zip[0][1]
            named_color_count[tmp_color] += 1
        named_colors = sorted(
            named_color_count.items(), key=lambda x: x[1], reverse=True
        )
        named_colors = [(color, color_names[color]) for color, count in named_colors]
        return named_colors

    def _cb_lead_image_button(self):
        self.load_image()
        if not self.image:
            return
        self.graphicsView.display_image(self.image)
