from core.tools.tool import Tool

class Eyedropper(Tool):
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def sample(self, canvas, x, y):
        texture = canvas.top_texture
        w, h = texture.size
        half_size = 2

        left = max(0, x - half_size)
        upper = max(0, y - half_size)
        right = min(w, x + half_size + 1)
        lower = min(h, y + half_size + 1)

        region = texture.crop((left, upper, right, lower))
        pixel_values = list(region.getdata())

        avg = (
            sum(p[0] for p in pixel_values) / len(pixel_values),
            sum(p[1] for p in pixel_values) / len(pixel_values),
            sum(p[2] for p in pixel_values) / len(pixel_values)
        )
        return avg