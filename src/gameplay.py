#!/usr/bin/env python3.6
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


# setup
pygame.init()
clock = pygame.time.Clock()
pygame.key.set_repeat(10, 100)
screen = pygame.display.set_mode(SCREENRECT.size)
pygame.display.set_caption(" Slip the Virus ")

Img.background = load_image("background.gif")
background = pygame.Surface(SCREENRECT.size)
for x in range(0, SCREENRECT.width, Img.background.get_width()):
    background.blit(Img.background, (x, 0))
background_rect = background.get_rect()


# The key master, holder.
holder = Holder(
    unicorn=Unicorn("unicorn.png", spawn_location={"midleft": (50, 640 // 2)}),
    hearts_holder=[],
    virus_holder=[],
    stats=StatsBar(),
)

# main game loop
while holder.unicorn.alive == bool(1):

    if holder.unicorn.dead_scene_time <= 0:
        holder.stats.final_points = holder.stats.get_current_game_time()
        holder.unicorn.alive = False

    holder.dirtyrects.append(screen.blit(background, (0, 0)))

    for event in pygame.event.get():
        pygame.event.pump()
        key = pygame.key.get_pressed()
        holder.unicorn.state(key, screen)

        if key[K_ESCAPE]:
            exit(1)

        if key[K_PAUSE]:
            pause_text, pause_text_position = writer(
                phrase="PAUSE",
                font="ubuntumono",
                size=30,
                color=(0, 255, 0),
                where={"center": (400, 200)},
            )
            holder.dirtyrects.append(screen.blit(pause_text, pause_text_position))
            pygame.display.update()
            pygame.time.wait(5000)

        if event.type == pygame.QUIT:
            exit(1)

    o_o = holder.unicorn.rect.collidelist(holder.hearts_holder)
    x_x = holder.unicorn.rect.collidelist(holder.virus_holder)

    if x_x != -1:
        if holder.unicorn.shield == True:
            holder.virus_holder[x_x].death_scene()
            holder.virus_holder[x_x].dead = True
            holder.stats.viruses_eliminated += 1
        elif holder.unicorn.shield == False:
            if not holder.unicorn.health_ok():
                holder.unicorn.dead = True
                holder.unicorn.death_scene()
            else:
                holder.unicorn.hit = True

    if o_o != -1:
        if holder.hearts_holder[o_o].full:
            holder.hearts_holder[o_o].consume(holder.unicorn)

    Heart.replicate(holder.stats.get_current_game_time(), holder)
    Virus.replicate(holder.stats.get_current_game_time(), holder)

    for host in holder.virus_holder:
        host.update(holder)

    for host in holder.virus_holder:
        host.draw(screen, holder)

    for host in holder.virus_holder:
        if host.dead and host.death_scene_time <= 0:
            host.erase(screen, background, holder)

    for host in holder.hearts_holder:
        host.update(holder)

    for host in holder.hearts_holder:
        host.draw(screen, holder)

    for host in holder.hearts_holder:
        if not host.full and host.vanish_time <= 0:
            host.erase(screen, background, holder)

    holder.unicorn.update(screen, holder)
    holder.unicorn.draw(screen, holder)
    holder.stats.update(screen, holder)

    pygame.display.update(holder.dirtyrects)
    holder.reset_dirtyrects()
    clock.tick(69)


print(
    f"""
+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + 

Game stats (*_*)

+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + 

Total time lasted        => {holder.stats.final_points}
Total viruses eliminated => {holder.stats.viruses_eliminated}

+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + 
"""
)
