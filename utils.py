# csr

import os

from PIL import Image

from config import images_path


class Img:
    """Contenedor de imagenes."""
    pass


def mirror_image(image, saved_location):
    """
    Transpose una imagen para usarla cada que el jugador quiera moverse
    a la izquierda; para que no se vea rancio.
    """

    to_mirror = Image.open(os.path.join(images_path, image))
    mirrored = to_mirror.transpose(Image.FLIP_LEFT_RIGHT)
    mirrored.save(os.path.join(images_path, saved_location))
    mirrored.show()