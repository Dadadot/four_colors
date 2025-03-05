from typing import List, Optional
from four_colors import Signals

from PySide6.QtCore import QPointF, Qt, QSize, QRectF
from PySide6.QtGui import QBrush, QPen, QMouseEvent, QColor, QPixmap, QImage
from PySide6.QtWidgets import (
    QGraphicsScene,
    QGraphicsView,
    QGraphicsRectItem,
    QGraphicsPixmapItem,
)

from enum import Enum, auto


class GVStates(Enum):
    MEASURE = auto()
    SELECT = auto()


class RefGVStates:
    text_display = {GVStates.MEASURE: "Measure", GVStates.SELECT: "Edit"}

    @staticmethod
    def by_clear_text(text_display: str) -> Optional[GVStates]:
        # perfection
        try:
            state = [
                k for k, v in RefGVStates.text_display.items() if v == text_display
            ][0]
            return state
        except:
            return None


class CostumGraphicsView(QGraphicsView):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))
        self.image_graphics_pixmap: QGraphicsPixmapItem
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Set transformations to be disabled (no scaling or panning)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        # self.image_graphics_pixmap.


    def display_image(self, image: QImage):
        image_pixmap = QPixmap(image)
        self.scene().clear()
        self.image_graphics_pixmap = self.scene().addPixmap(image_pixmap)
        self.scene().setSceneRect(0, 0, image_pixmap.width(), image_pixmap.height())
        self.fitInView(self.image_graphics_pixmap, Qt.AspectRatioMode.KeepAspectRatio)


class SelectionGraphicsView(CostumGraphicsView):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.selection_point_start: QPointF
        self.selection_point_end: QPointF
        self.selection_rect: Optional[QGraphicsRectItem] = None
        self._state = GVStates.SELECT

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_point = self.mapToScene(event.position().toPoint())
            self.dragging = True

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging:
            self.end_point = self.mapToScene(event.position().toPoint())
            self._update_selection_rect()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.end_point = self.mapToScene(event.position().toPoint())
            self.dragging = False
            Signals.RectangleSelected.emit(self.selection_rect.rect())
            self._clear_selection_rect()

    def _clear_selection_rect(self):
        """Removes the temporary rectangle from the scene."""
        if self.selection_rect:
            self.scene().removeItem(self.selection_rect)
            self.selection_rect = None

    def _update_selection_rect(self):
        """Draws a temporary rectangle during mouse drag."""
        if not all([self.start_point, self.end_point]):
            return
        rect = QRectF(self.start_point, self.end_point).normalized()
        if not self.selection_rect:
            pen = QPen(QColor(0, 0, 255))
            brush = QBrush(QColor(0, 0, 255, 50))
            self.selection_rect = self.scene().addRect(rect, pen, brush)
        else:
            self.selection_rect.setRect(rect)
