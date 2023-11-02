from core.tools.tool import Tool

class BrushTool(Tool):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.brush_size = 1
        return cls._instance

    # Paint the pixels in the square with top left corner (x,y) and side brush_size
    def paint(self, x, y, color, canvas):
        half_size = self.brush_size // 2
        for i in range(x, x + self.brush_size):
            for j in range(y, y + self.brush_size):
                canvas.set_pixel((i, j), color)

    def set_brush_size(self, size):
        self._instance.brush_size = size