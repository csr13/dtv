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
# Background

Img.background = load_image("background.gif")

background = pygame.Surface(SCREENRECT.size)
for x in range(0, SCREENRECT.width, Img.background.get_width()):
    background.blit(Img.background, (x, 0))
background_rect = background.get_rect()

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Characters

unicorn = Unicorn("unicorn.png", spawn_location={"center": (640 // 2, 480 // 2)})

holder = Holder(unicorn_holder=[unicorn], virus_holder=[])

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Main Loop

while bool(1):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(1)

        pygame.event.pump()
        key = pygame.key.get_pressed()
        unicorn.state(key, screen)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Handle the background first

    holder.dirtyrects.append(screen.blit(background, (0, 0)))

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Handle Viruses

    if not int(random.random() * 42):
        holder.virus_holder.append(Virus("virus.gif"))

    for host in holder.virus_holder:
        host.erase(screen, background, holder)
        host.update()

    for each in holder.virus_holder:
        each.draw(screen, holder)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Handle Unicorns

    holder.unicorn_holder[0].update(screen, holder)
    holder.unicorn_holder[0].draw(screen, holder)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Update game & clear rects

    pygame.display.update(holder.dirtyrects)
    holder.reset_dirtyrects()
    clock.tick(50)
