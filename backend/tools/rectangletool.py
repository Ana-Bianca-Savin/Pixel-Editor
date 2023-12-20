from backend.tools.tool import Tool

class RectangleTool(Tool):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.stroke_weight = 1
            cls._instance.fill = False
            cls._instance.fill_color = None
            cls._instance.stroke_color = (0, 0, 0, 255)
            cls._instance.drawing = False
            cls._instance.origin = (0, 0)
        return cls._instance
    
    def draw_rectangle(self, canvas, top_left, bottom_right):
        if self._instance.fill is True:
            canvas.draw_rectangle(top_left, bottom_right, self._instance.fill_color , self._instance.stroke_color, self._instance.stroke_weight)
        else:
            canvas.draw_rectangle(top_left, bottom_right, None , self._instance.stroke_color, self._instance.stroke_weight)

    def set_stroke_weight(self, w):
        self._instance.stroke_weight = w

    def set_stroke_color(self, c):
        self._instance.stroke_color = c

    def set_fill(self, f):
        self._instance.fill = f

    def set_fill_color(self, c):
        self._instance.fill_color = c

    def set_drawing_state(self, state : bool):
        self.drawing = state

    def get_drawing_state(self):
        return self.drawing
    
    def set_origin(self, origin):
        self.origin = origin

    def get_origin(self):
        return self.origin