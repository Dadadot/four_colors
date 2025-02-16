from typing import List, Optional

from PySide6.QtCore import QPointF, Qt, QSize, QRectF
from PySide6.QtGui import QBrush, QPen, QMouseEvent, QColor, QPixmap, QImage
from PySide6.QtWidgets import (
    QGraphicsEllipseItem,
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
        # self.scene().setSceneRect(0, 0, 500, 500)
        self.selection_point_start: QPointF
        self.selection_point_end: QPointF
        self.selection_rect: Optional[QGraphicsRectItem]
        self._state = GVStates.SELECT
        self.setFixedSize(QSize(500, 500))
        # Disable scrollbars
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        # Set transformations to be disabled (no scaling or panning)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.image_graphics_pixmap.

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
            self._clear_selection_rect()  # Remove the temporary rectangle

    def display_image(self, image: QImage):
        image_pixmap = QPixmap(image)
        self.image_graphics_pixmap = self.scene().addPixmap(image_pixmap)

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

    def _fit_image_to_view(self, pixmap_item):
        # Get the image size and the view size
        pixmap = pixmap_item.pixmap()
        view_rect = self.viewport().rect()
        pixmap_size = pixmap.size()
        scale = min(
            view_rect.width() / pixmap_size.width(),
            view_rect.height() / pixmap_size.height(),
        )

        # Scale the pixmap to fit the view while maintaining the aspect ratio
        pixmap_item.setScale(scale)

        # Center the image in the view
        self.centerOn(pixmap_item)
