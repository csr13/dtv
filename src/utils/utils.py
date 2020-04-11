# Copyright 2020 C. Sanchez Roman
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import random
import sys

sys.path.append("..")

import pygame
from PIL import Image

from config import IMAGES_PATH


def load_image(file, transparent=None):
    """
    Cargador de imagenes.
    """

    file = os.path.join(IMAGES_PATH, file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pygame.get_error()))
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

    to_mirror = Image.open(os.path.join(IMAGES_PATH, image))
    mirrored = to_mirror.transpose(Image.FLIP_LEFT_RIGHT)
    mirrored.save(os.path.join(IMAGES_PATH, drop_location))
    mirrored.show()


