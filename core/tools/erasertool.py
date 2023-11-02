from core.tools.tool import Tool

class EraserTool(Tool):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.eraser_size = 1
        return cls._instance

    # Erase the pixels in the square with top left corner (x,y) and side eraser_size
    def erase(self, x, y, canvas):
        half_size = self.eraser_size // 2
        for i in range(x, x + self.eraser_size):
            for j in range(y, y + self.eraser_size):
                canvas.set_pixel((i, j), (0, 0, 0, 0))

    def set_eraser_size(self, size):
        self._instance.eraser_size = size