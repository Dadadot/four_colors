from .view.ui_compiled.main import Ui_MainWindow
from collections import defaultdict
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsPixmapItem, QGraphicsScene
from PySide6.QtGui import QPixmap, QImage, QColor



class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

class FileBrowser:
    @staticmethod
    def load_image(parent) -> str:
        file_name, _ = QFileDialog.getOpenFileName(
        parent, 
        'Open Image File', 
        '', 
        'Images (*.png *.xpm *.jpg *.jpeg *.bmp *.gif)'  # Add more image formats if needed
        )
        return file_name

class App:
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        self.graphic_scene = QGraphicsScene()
        self.window.graphicsView.setScene(self.graphic_scene)
        self.window.pushButton.clicked.connect(lambda: self.load_image())

    def run(self) -> QApplication:
        self.window.show()
        sys.exit(self.app.exec())
    
    def quit(self):
        self.app.quit()

    def load_image(self):
        file_browser = FileBrowser
        file_path = file_browser.load_image(self.window)
        if not file_path:
            return
        pixmap = QPixmap(file_path)
        pixmap_item = QGraphicsPixmapItem(pixmap)
        self.graphic_scene.addItem(pixmap_item)
        self.fit_image_to_view(pixmap_item)
        self.extract_prominent_colors(file_path)

    def fit_image_to_view(self, pixmap_item):
        # Get the image size and the view size
        pixmap = pixmap_item.pixmap()
        view_rect = self.window.graphicsView.viewport().rect()
        pixmap_size = pixmap.size()

        # Scale the pixmap to fit the view while maintaining the aspect ratio
        pixmap_item.setScale(min(view_rect.width() / pixmap_size.width(), view_rect.height() / pixmap_size.height()))

        # Center the image in the view
        self.window.graphicsView.centerOn(pixmap_item)


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
        for w in sorted(le_colors.items(), key=lambda x: x[1], reverse=True):
            i += 1
            print(w)
            if i == 4:
                break
