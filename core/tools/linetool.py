from core.tools.tool import Tool

class LineTool(Tool):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.stroke_weight = 1
        return cls._instance
    
    def set_line_width(self, w):
        self._instance.stroke_weight = w
    
    def draw_line(self, canvas, start, end, color):
        canvas.draw_line(start, end, color, self._instance.stroke_weight)