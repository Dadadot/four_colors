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
from . import Signals, ColorThing


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)


class App:
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        self.color_thing = ColorThing()
        self.graphicsView = SelectionGraphicsView()
        self.selection_graphicsView = CostumGraphicsView()
        self.image: Optional[QImage] = None

        self.window.c_image_main.layout().addWidget(self.graphicsView)
        self.window.c_image_selection.layout().addWidget(self.selection_graphicsView)
        self.window.actionLoad.triggered.connect(self._cb_load_image_button)
        Signals.RectangleSelected.connect(self._on_rectangel_selected)

        self.color_widgets = []
        for i in range(4):
            x = WidgetColor("No Name", (0, 0, 0))
            self.window.c_colors.layout().addWidget(x)
            self.color_widgets.append(x)

    def run(self) -> QApplication:
        self.window.show()
        sys.exit(self.app.exec())

    def quit(self):
        self.app.quit()

    # Callbacks

    def _cb_load_image_button(self):
        self._load_image()
        if not self.image:
            return
        self.graphicsView.display_image(self.image)

    def _on_rectangel_selected(self, rect: QRectF):
        if not self.image:
            return
        x = self.image.copy(rect.toRect())
        self.selection_graphicsView.display_image(x)
        colors = self.color_thing.extract_colors(x)
        named_colors = self.color_thing.get_named_colors(colors)
        self._update_color_widgets(named_colors)

    # Private

    def _update_color_widgets(self, colors):
        for i, item in enumerate(colors):
            if i == 4:
                break
            rgb, name = item
            w = self.color_widgets[i]
            w.set_color(name, rgb)

    def _load_image(self):
        file_path = self._get_image_path()
        image = QImage(file_path)
        if image.format() != QImage.Format.Format_RGB888:
            image = image.convertToFormat(QImage.Format.Format_RGB888)
        self.image = image

    def _get_image_path(self) -> str:
        file_name, _ = QFileDialog.getOpenFileName(
            None,
            "Open Image File",
            "",
            "Images (*.png *.xpm *.jpg *.jpeg *.bmp *.gif *.webp)",  # Add more image formats if needed
        )
        return file_name
