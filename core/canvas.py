from PIL import Image
from core.layer import Layer, BlendingMode

# A canvas stores an array of layers,
# the preview of all the layers combined (called top_texture here)
# and the index of the actively selected layer.

class Canvas:
    def __init__(self, size):
        self.layers = []
        self.size = size
        self.top_texture = Image.new("RGBA", size, (0, 0, 0, 0))
        self.__active_layer_index = 0

    def add_layer(self, blending_mode=BlendingMode.NORMAL, background_color=None):
        layer = Layer(self.size, blending_mode, None, background_color)
        self.layers.append(layer)

        self.update_top_texture()

    def set_active_layer(self, new_layer_index):
        # Is this new index a valid layer?
        if new_layer_index >= 0 and new_layer_index < len(self.layers):
            self.__active_layer_index = new_layer_index
        else:
            raise ValueError("Wrong layer index provided")

    # Set the pixel color of a point on the active layer.
    # This must also trigger an update to the preview since we made a modification
    def set_pixel(self, point, new_color):
        self.layers[self.__active_layer_index].set_pixel(point, new_color)
        self.update_top_texture()

    def draw_line(self, start, end, color, stroke_weight):
        self.layers[self.__active_layer_index].draw_line(start, end, color, stroke_weight)
        self.update_top_texture()

    def draw_rectangle(self, top_left, bottom_right, fill_color, stroke_color, stroke_weight):
        self.layers[self.__active_layer_index].draw_rectangle(top_left, bottom_right, fill_color, stroke_color, stroke_weight)
        self.update_top_texture()

    def set_top_texture(self, texture):
        self.top_texture = texture

    def merge_layers(self):
        merged = Image.new("RGBA", self.size, (0, 0, 0, 0))
        for layer in self.layers:
            merged = Image.alpha_composite(merged, layer.texture)
        return merged

    def update_top_texture(self):
        self.top_texture = self.merge_layers()
