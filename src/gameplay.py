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
import pdb

import pygame
from pygame.locals import *

from characters import *
from config import PUNTAJE, SCREENRECT, VIDAS
from utils import load_image, Img, writer

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Inits

pygame.init()
clock = pygame.time.Clock()
pygame.key.set_repeat(10, 100)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Pantalla

screen = pygame.display.set_mode(SCREENRECT.size)
pygame.display.set_caption("<[*_*]> Space Unicorn")

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Texto

score, score_position = writer(
    phrase=f"Puntos: {PUNTAJE}",
    font="ubuntumono",
    size=20,
    color=(102, 255, 102),
    where={"top": 10, "right": 110},
)

vidas, vidas_position = writer(
    phrase=f"Vidas: ",
    font="ubuntumono",
    size=20,
    color=(102, 255, 102),
    where={"top": 10, "right": 200},
)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Background

Img.background = load_image("background.gif")

background = pygame.Surface(SCREENRECT.size)
for x in range(0, SCREENRECT.width, Img.background.get_width()):
    background.blit(Img.background, (x, 0))
background_rect = background.get_rect()

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Load player lives, this needs to be converted to a class and inherited to
# the Uniconrn

Img.heart = load_image("heart.png")
courage_meter = []
padding = [2, 195]
padding_copy = padding[:]

for each in range(VIDAS):

    courage_load = Img.heart
    courage_meter.append(courage_load.get_rect())
    courage_meter[each].x = padding[1]
    courage_meter[each].y = padding[0]
    background.blit(courage_load, courage_meter[each])
    padding[1] += 35


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Imagenes

holder = Holder(unicorn_holder=[], virus_holder=[])

unicorn = Unicorn("unicorn.png", spawn_location={"center": (640 // 2, 480 // 2)})

virus = Virus("virus.gif")

holder.unicorn_holder.append(unicorn)
holder.virus_holder.append(virus)

# unicorn.rect = unicorn.image.get_rect(center=posicion_init)


def main():
    global SCREENRECT
    while bool(1):
        shield, rotate = (
            False,
            False,
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(1)

            pygame.event.pump()
            key = pygame.key.get_pressed()
            unicorn.state(key, screen)

            if not int(random.random() * 5):
                holder.virus_holder.append(Virus("virus.gif"))

        screen.blit(background, (0, 0))
        background.blit(score, score_position)
        background.blit(vidas, vidas_position)

        holder.unicorn_holder[0].draw(screen)

        for each in holder.virus_holder:
            each.update()
            each.draw(screen)

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
