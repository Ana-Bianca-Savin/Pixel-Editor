from core.tools.tool import Tool
from enum import Enum

class BrushType(Enum):
    SQUARE = 1
    ROUND = 2
    CUSTOM = 3

class BrushTool(Tool):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.brush_size = 1
            cls._instance.brush_type = BrushType.ROUND
        return cls._instance

    # Paint the pixels with the brush, depending on its type
    def paint(self, canvas, x, y, color):

        if self.get_brush_size() == 1:
                canvas.set_pixel((x, y), color)
                return

        if self.brush_type is BrushType.SQUARE:
            # First calculate the top left corner
            x = x - self.brush_size // 2
            y = y - self.brush_size // 2
            canvas.draw_rectangle((x, y), (x + self.brush_size, y + self.brush_size), color, (0, 0, 0, 0), 0)
            return
        
        if self.brush_type is BrushType.ROUND:
            canvas.draw_ellipse((x, y), (self.brush_size // 2, self.brush_size // 2), color, (0, 0, 0, 0), 0)
            return

    def set_brush_size(self, size):
        self._instance.brush_size = size

    def set_brush_type(self, type):
        self._instance.brush_type = type

    def get_brush_size(self):
        return self._instance.brush_size
