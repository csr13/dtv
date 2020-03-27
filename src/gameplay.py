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

import math
import os
import random
import time
import pdb

import pygame
from pygame.locals import *

from characters import *
from config import SCREENRECT
from utils import load_image, Img, writer

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Inits

pygame.init()
clock = pygame.time.Clock()
pygame.key.set_repeat(10, 100)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Pantalla

screen = pygame.display.set_mode(SCREENRECT.size)
pygame.display.set_caption(" Inf3Kt!0n ")

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Background

Img.background = load_image("background.gif")

background = pygame.Surface(SCREENRECT.size)
for x in range(0, SCREENRECT.width, Img.background.get_width()):
    background.blit(Img.background, (x, 0))
background_rect = background.get_rect()

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# The key master, holder.

holder = Holder(
    unicorn=Unicorn("unicorn.png", spawn_location={"midleft": (50, 640 // 2)}),
    virus_holder=[],
    stats=StatsBar(),
)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Main Loop

# Points are calculated by the amount of seconds that the player lasted in the
# gameplay, from the moment the loop starts, till the moment the player gets hit

start_points = math.ceil(time.time())
virus_killed = 0

while holder.unicorn.alive == True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(1)

        pygame.event.pump()
        key = pygame.key.get_pressed()
        holder.unicorn.state(key, screen)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Handle the background first

    holder.dirtyrects.append(screen.blit(background, (0, 0)))
    holder.stats.generate(screen, holder.unicorn.shield_energy, holder)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Handle Viruses

    if not int(random.random() * 40):
        holder.virus_holder.append(Virus("virus.gif"))

    for host in holder.virus_holder:
        host.update()
        host.draw(screen, holder)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Detect collisions

    x_x = holder.unicorn.rect.collidelist(holder.virus_holder)
    if x_x != -1:
        if holder.virus_holder[x_x].dead:
            pass
        elif holder.unicorn.shield == True:
            virus_killed += 1
            holder.virus_holder[x_x].dead = True
        elif holder.virus_holder[x_x].dead == False:
            holder.unicorn.death_scene()
            holder.unicorn.dead = True

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Handle Unicorns

    holder.unicorn.update(screen, holder)
    holder.unicorn.draw(screen, holder)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Check who is dead.

    for virus in holder.virus_holder:
        if virus.dead and virus.dead_time < 0:
            virus.erase(screen, background, holder)

    if holder.unicorn.dead and holder.unicorn.dead_time < 0:
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Have the stats ready to be displayed here.
        holder.unicorn.alive = False

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Update game & clear rects

    pygame.display.update(holder.dirtyrects)
    holder.reset_dirtyrects()
    clock.tick(50)
