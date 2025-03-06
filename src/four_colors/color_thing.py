from PySide6.QtGui import QImage, QColor
from collections import defaultdict


class ColorThing:
    def extract_colors(self, image: QImage):
        le_colors = defaultdict(int)
        for y in range(image.height()):
            for x in range(image.width()):
                color = QColor(image.pixel(x, y))
                color_tuple = color.getRgb()[:3]
                le_colors[color_tuple] += 1
        le_colors_sorted = sorted(le_colors.items(), key=lambda x: x[1], reverse=True)
        le_colors_sorted = [color for color, _ in le_colors_sorted]
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
        named_colors = [(color, color_names[color]) for color, _ in named_colors]
        return named_colors
