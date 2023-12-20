from PIL import Image, ImageOps

class Transform:

    @staticmethod
    def flip_vertically(texture: Image.Image) -> Image.Image:
        return ImageOps.flip(texture)
    @staticmethod
    def flip_horizontally(texture: Image.Image) -> Image.Image:
        return ImageOps.mirror(texture)

    @staticmethod
    def translate(texture: Image.Image, x: int, y: int) -> Image.Image:
        return texture.transpose(Image.Transpose.MOVE, (x, y))

    @staticmethod
    def rotate(texture: Image.Image, angle: float, resample_filter=None) -> Image.Image:
        if resample_filter is None:
            return texture.rotate(angle)
        return texture.rotate(angle, resample_filter)
    
    @staticmethod
    def scale(texture: Image.Image, new_size: tuple[int, int]) -> Image.Image:
        return texture.resize(new_size, Image.NEAREST)