from PIL import Image
from core.layer import Layer, BlendingMode
from core.utilties import export

# A canvas stores an array of layers,
# the preview of all the layers combined (called top_texture here)
# and the index of the actively selected layer.

class Canvas:
    def __init__(self, size):
        self.layers = []
        self.size = size
        self.top_texture = Image.new("RGBA", size, (0, 0, 0, 0))
        self.__active_layer_index = 0
        self.preview_layer = Layer(size, BlendingMode.NORMAL)

    def get_active_layer_index(self):
        return self.__active_layer_index

    def add_layer(self, blending_mode=BlendingMode.NORMAL, fill_color=None):
        layer = Layer(self.size, blending_mode, None, fill_color)
        self.layers.append(layer)

        self.update_top_texture()

    def delete_layer(self, index):
        self.layers.pop(index)
        
        self.update_top_texture()

    def place_texture(self, texture: Image.Image,
                      center: tuple[int, int]):
        self.layers[self.__active_layer_index].place_texture(texture, center)
        self.update_top_texture()

    def set_active_layer(self, new_layer_index):
        # Is this new index a valid layer?
        if new_layer_index >= 0 and new_layer_index < len(self.layers):
            self.__active_layer_index = new_layer_index
        else:
            raise ValueError("Wrong layer index provided")
        
    def get_active_layer(self):
        return self.layers[self.__active_layer_index]
    
    def flood_fill(self, seed, color):
        self.layers[self.__active_layer_index].flood_fill(seed, color)
        self.update_top_texture()

    # Set the pixel color of a point on the active layer.
    # This must also trigger an update to the preview since we made a modification
    def set_pixel(self, point, new_color):
        self.layers[self.__active_layer_index].set_pixel(point, new_color)
        self.update_top_texture()

    def get_pixel(self, point):
        return self.layers[self.__active_layer_index].get_pixel(point)

    def draw_line(self, start, end, color, stroke_weight):
        self.layers[self.__active_layer_index].draw_line(start, end, color, stroke_weight)
        self.update_top_texture()

    def draw_rectangle(self, top_left, bottom_right, fill_color, stroke_color, stroke_weight):
        self.layers[self.__active_layer_index].draw_rectangle(top_left, bottom_right, fill_color, stroke_color, stroke_weight)
        self.update_top_texture()

    def draw_ellipse(self, center, axis, fill_color, stroke_color, stroke_weight):
        self.layers[self.__active_layer_index].draw_ellipse(center, axis, fill_color, stroke_color, stroke_weight)
        self.update_top_texture()

    def set_top_texture(self, texture):
        self.top_texture = texture

    def merge_layers(self):
        merged = Image.new("RGBA", self.size, (0, 0, 0, 0))
        for layer in self.layers:
            merged = Image.alpha_composite(merged, layer.texture)
        merged.alpha_composite(self.preview_layer.texture)
        return merged

    def update_top_texture(self):
        self.top_texture = self.merge_layers()

    def copy(self):
        new_canvas = Canvas(self.size)
        for layer in self.layers:
            new_canvas.layers.append(layer.copy())
        new_canvas.__active_layer_index = self.__active_layer_index
        new_canvas.update_top_texture()
        return new_canvas
