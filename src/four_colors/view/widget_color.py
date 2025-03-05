from four_colors.view.ui_compiled.w_color import Ui_Form
from typing import Tuple
from PySide6.QtWidgets import QWidget


class WidgetColor(QWidget, Ui_Form):
    def __init__(self, color_name: str, rgb: Tuple[int, int, int]) -> None:
        super().__init__()
        self.setupUi(self)
        self.label.setText(color_name)
        self._set_button_color(rgb)


    def set_color(self, color_name: str, rgb: Tuple[int, int, int]):
        self.label.setText(color_name)
        self._set_button_color(rgb)

    def _set_button_color(self, rgb: Tuple[int, int, int]):
        """Set the button's background color using the provided RGB values."""
        r, g, b = rgb
        self.pushButton.setStyleSheet(f"background-color: rgb({r}, {g}, {b});")
