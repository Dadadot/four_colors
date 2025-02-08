from typing import List

from PySide6.QtCore import QPointF, Qt, QSize
from PySide6.QtGui import QBrush, QPen
from PySide6.QtWidgets import (
    QGraphicsEllipseItem,
    QGraphicsScene,
    QGraphicsView,
)

from enum import Enum, auto


class GVStates(Enum):
    new = auto()
    select = auto()


class RefGVStates:
    clear_text = {GVStates.new: "New", GVStates.edit: "Edit"}

    @staticmethod
    def by_clear_text(clear_text):
        try:
            state = [k for k, v in RefGVStates.clear_text.items() if v == clear_text][0]
            return state
        except:
            return None


class GraphicsView(QGraphicsView):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))
        self.scene().setSceneRect(0, 0, 500, 500)
        self.control_points_main = []
        self.control_points_off = []
        self._state = GVStates.new
        self.setFixedSize(QSize(500, 500))
        # Disable scrollbars
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        # Set transformations to be disabled (no scaling or panning)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.NoAnchor)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    def fit_image_to_view(self, pixmap_item):
        # Get the image size and the view size
        pixmap = pixmap_item.pixmap()
        view_rect = self.window.graphicsView.viewport().rect()
        pixmap_size = pixmap.size()
        scale = min(
            view_rect.width() / pixmap_size.width(),
            view_rect.height() / pixmap_size.height(),
        )

        # Scale the pixmap to fit the view while maintaining the aspect ratio
        pixmap_item.setScale(scale)

        # Center the image in the view
        self.window.graphicsView.centerOn(pixmap_item)

    def mousePressEvent(self, event):
        if self.state == GVStates.new:
            if event.button() == Qt.MouseButton.LeftButton:
                click_position = self.mapToScene(event.pos())
                x, y = click_position.x(), click_position.y()
                cp = ControlPoint(x, y)
                self.scene().addItem(cp)
                self.control_points_main.append(cp)
        elif self.state == GVStates.edit:
            super().mousePressEvent(event)

    def draw_dot(self, position: QPointF):
        dot = QGraphicsEllipseItem(-2.5, -2.5, 5, 5)
        dot.setBrush(QBrush(Qt.GlobalColor.black))
        dot.setPen(QPen(Qt.PenStyle.NoPen))
        dot.setPos(position)

    def push_my_buttons(self):
        control = [x.pos().toTuple() for x in self.control_points_main]
        # tuples, no deepcopy
        control2 = [v for v in control][::-1]
        startx, starty = control.pop(0)
        start = ControlPoint(startx, starty)
        targetx, targety = control.pop(-1)
        target = ControlPoint(targetx, targety)

        control2 = [
            ((v[0] + startx + targetx) / 3, (v[1] + starty + targety) / 3)
            for v in control
        ]
        for c in control2:
            x, y = c
            cp = ControlPoint(x, y)
            self.scene().addItem(cp)
            self.control_points_off.append(cp)

        c = Curve(self.control_points_main, self.control_points_off)
        self.scene().addItem(c)
        self.cache_polygon = []
