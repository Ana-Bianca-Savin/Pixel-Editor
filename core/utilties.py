from PIL import Image

def export(texture: Image.Image, 
           format: str, 
           size: tuple[int, int], 
           resize_algorithm: int, 
           file_name: str) -> None:
    resized_texture = texture.resize(size, resample=resize_algorithm)
    resized_texture.save(file_name, format=format)

def import_texture(file_path: str) -> Image.Image:
    texture = Image.open(file_path).convert('RGBA')
    return texture
