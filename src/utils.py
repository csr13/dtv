import os

import pygame
from PIL import Image

from config import images_path


class Img:
    """Contenedor de imagenes."""
    pass


def load_image(file, transparent=None):
    """
    Cargador de imagenes.
    """

    file = os.path.join(images_path, file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' %
                         (file, pygame.get_error()))
    if transparent:
        corner = surface.get_at((0, 0))
        surface.set_colorkey(corner, RLEACCEL)
    return surface


def writer(phrase=None, font=None, size=None, color=None, where=None):
    """
    Esta funcion necesita algo de trabajo, pero funciona, y su uso es
    sencillo, crea un SysFont objeto y regresa un tuple para blitearlo
    a la pantalla.
    """

    if phrase and font and size and color and where:
        to_write = pygame.font.SysFont(font, size)
        to_write = to_write.render(phrase, 2, color)
        position = to_write.get_rect(**where)
        return to_write, position


def flip_img(image, drop_location):
    """
    Transpose una imagen para usarla cada que el jugador quiera moverse
    a la izquierda; para que no se vea rancio.
    """

    to_mirror = Image.open(os.path.join(images_path, image))
    mirrored = to_mirror.transpose(Image.FLIP_LEFT_RIGHT)
    mirrored.save(os.path.join(images_path, drop_location))
    mirrored.show()