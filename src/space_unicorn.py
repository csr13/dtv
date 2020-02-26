import os
import pdb

import pygame
from pygame.locals import *

from characters import Unicorn
from config import (CHECK, PUNTAJE, SCREENRECT, VIDAS)
from utils import load_image, Img, writer


# Inits =======================================================================
pygame.init()
clock = pygame.time.Clock()
pygame.key.set_repeat(10,100)

# Pantalla ====================================================================
screen = pygame.display.set_mode((480, 480))
pygame.display.set_caption("<[*_*]> Space Unicorn")

# Texto =======================================================================
score, score_position = writer(
    phrase=f"Puntos: {PUNTAJE}",
    font="ubuntumono",
    size=20,
    color=(102, 255, 102),
    where={"top" : 10, "right" : 110}
)

vidas, vidas_position = writer(
    phrase=f"Vidas: ",
    font="ubuntumono",
    size=20,
    color=(102,255,102),
    where={"top" : 10, "right" : 200}
)

# Background ==================================================================
Img.background = load_image("background.gif")

background = pygame.Surface(SCREENRECT.size)
for x in range(0, SCREENRECT.width, Img.background.get_width()):
    background.blit(Img.background, (x, 0))
background_rect = background.get_rect()

# Carga las vidas de el jugador a la pantalla. ================================
Img.heart      = load_image("heart.png")
courage_meter  = []
padding        = [2, 195]
padding_copy   = padding[:] 

for each in range(VIDAS):

    courage_load = Img.heart
    courage_meter.append(courage_load.get_rect())
    courage_meter[each].x = padding[1]
    courage_meter[each].y = padding[0]
    background.blit(courage_load, courage_meter[each])
    padding[1] += 35

# Imagenes ====================================================================
posicion_init  = (480//2, 480//2)
unicorn        = Unicorn("unicorn.png")
unicorn.rect   = unicorn.image.get_rect(center=posicion_init)


def main():
    while bool(1):
        shield, rotate = (False, False,)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(1)

            pygame.event.pump()
            key = pygame.key.get_pressed()
            unicorn.state(key, screen)
        
        screen.blit(background, (0,0))
        background.blit(score, score_position)
        background.blit(vidas, vidas_position)

        unicorn.update(screen)

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
