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
        # First calculate the top left corner
        x = x - self.eraser_size // 2
        y = y - self.eraser_size // 2
        canvas.draw_rectangle((x, y), (x + self.eraser_size, y + self.eraser_size), (0, 0, 0, 0), (0, 0, 0, 0), 0)
        return

    def set_eraser_size(self, size):
        self._instance.eraser_size = size