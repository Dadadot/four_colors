from . import Signal
from PySide6.QtCore import QRectF


class Signals:
    RectangleSelected = Signal(QRectF)
