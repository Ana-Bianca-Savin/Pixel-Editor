from enum import Enum
from PIL import Image, ImageDraw

class BlendingMode(Enum):
    NORMAL = 1
    ADD = 2
    MULTIPLY = 3
    SCREEN = 4

class Layer:
    def __init__(self, layer_size, blending_mode=BlendingMode.NORMAL, texture=None, fill_color=None):
        self.layer_size = layer_size
        self.blending_mode = blending_mode

        # If no texture is provided in the constructor, just create a transparent texture
        if texture is None and fill_color is not None:
            self.texture = Image.new("RGBA", layer_size, fill_color)
        if texture is not None:
            self.texture = texture
        if texture is None and fill_color is None:
            self.texture = Image.new("RGBA", layer_size, (0, 0, 0, 0))
        self.__draw_object = ImageDraw.Draw(self.texture)

    def set_pixel(self, point, new_color):
        self.__draw_object.point(point, fill=new_color)

    def clear(self):
        empty_data = [(0, 0, 0, 0)] * (self.layer_size[0] * self.layer_size[1])
        self.texture.putdata(empty_data)

    def get_pixel(self, point):
        return self.texture.getpixel(point)

    def draw_line(self, start, end, color, stroke_weight):
        self.__draw_object.line([start, end], color, stroke_weight, None)

    def draw_rectangle(self, top_left, bottom_right, fill_color, stroke_color, stroke_weight):
        self.__draw_object.rectangle([top_left, bottom_right], fill_color, stroke_color, stroke_weight)

    def draw_ellipse(self, center, axis, fill_color, stroke_color, stroke_weight):
        # Calculate the bounding box
        left = center[0] - axis[0]
        top = center[1] - axis[1]
        right = center[0] + axis[0]
        bottom = center[1] + axis[1]
        self.__draw_object.ellipse([left, top, right, bottom], fill_color, stroke_color, stroke_weight)

    def place_texture(self, texture: Image.Image,
                      center: tuple[int, int]):
        left = center[0] - texture.size[0] // 2
        right = center[0] + texture.size[0] // 2
        top = center[1] - texture.size[1] // 2
        bottom = center[1] + texture.size[1] // 2

        alpha_mask = texture.split()[3]
        self.texture.paste(texture, [left, top, right, bottom], alpha_mask)