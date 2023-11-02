from enum import Enum
from PIL import Image, ImageDraw

class BlendingMode(Enum):
    NORMAL = 1
    ADD = 2
    MULTIPLY = 3
    SCREEN = 4

class Layer:
    def __init__(self, layer_size, blending_mode=BlendingMode.NORMAL, texture=None, background_color=None):
        self.layer_size = layer_size
        self.blending_mode = blending_mode

        # If no texture is provided in the constructor, just create a transparent texture
        if texture is None and background_color is not None:
            self.texture = Image.new("RGBA", layer_size, background_color)
        if texture is not None:
            self.texture = texture
        if texture is None and background_color is None:
            self.texture = Image.new("RGBA", layer_size, (0, 0, 0, 0))
        self.__draw_object = ImageDraw.Draw(self.texture)

    def set_pixel(self, point, new_color):
        self.__draw_object.point(point, fill=new_color)
