from PySide6.QtWidgets import QFileDialog, QGraphicsPixmapItem
from PySide6.QtGui import QPixmap

class ImageLoader:
    def get_image_path(self) -> str:
        file_name, _ = QFileDialog.getOpenFileName(
        None, 
        'Open Image File', 
        '', 
        'Images (*.png *.xpm *.jpg *.jpeg *.bmp *.gif *.webp)'  # Add more image formats if needed
        )
        return file_name

    def get_pixmap_item(self, image_path: str):
        pixmap = QPixmap(image_path)
        pixmap_item = QGraphicsPixmapItem(pixmap)
        return pixmap_item
