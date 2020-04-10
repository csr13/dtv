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

import os
import random
import time
import pdb

import pygame
from pygame.locals import *

from actors.characters import *
from config import SCREENRECT, SOUNDS_PATH
from utils.utils import load_image, writer


# Setup
pygame.init()
pygame.key.set_repeat(10, 100)
pygame.display.set_caption(" Slip the Virus ")
pygame.mixer.music.load(os.path.join(SOUNDS_PATH, "towel_defence.mp3"))
# pygame.mixer.music.play(-1, 0.0)

clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREENRECT.size)
img_background = load_image("background.gif")
background = pygame.Surface(SCREENRECT.size)

# Background
for x in range(0, SCREENRECT.width, img_background.get_width()):
    background.blit(img_background, (x, 0))
background_rect = background.get_rect()

# 'Stuff' holder
holder = Holder(
    unicorn=Unicorn("unicorn.png", spawn_location={"midleft": (50, 640 // 2)}),
    hearts_holder=[],
    virus_holder=[],
    potion_holder=[],
    stats=StatsBar(),
)


def main():
    """Main game loop"""

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

        # Collisions
        h_h = holder.unicorn.rect.collidelist(holder.hearts_holder)
        p_p = holder.unicorn.rect.collidelist(holder.potion_holder)
        x_x = holder.unicorn.rect.collidelist(holder.virus_holder)

        if x_x != -1:
            virus = holder.virus_holder[x_x]
            player = holder.unicorn
            if player.shield == False and not virus.dead:
                if not player.health_ok():
                    holder.unicorn.death_scene()
                elif not virus.hit_player:
                    virus.hit(screen, player, holder)
                elif virus.hit_player:
                    pass
            elif player.shield == True:
                player.kill_enemy(virus)

        if h_h != -1:
            heart = holder.hearts_holder[h_h]
            if heart.full:
                heart.consumed_scene(screen, background, holder)
                heart.full = False

        if p_p != -1:
            potion = holder.potion_holder[p_p]
            if potion.full:
                potion.consume(holder.unicorn)
                potion.full = False

        # Replications
        Heart.replicate(holder.stats.get_current_game_time(), holder)
        Potion.replicate(holder.stats.get_current_game_time(), holder)
        Virus.replicate(holder.stats.get_current_game_time(), holder)

        # Virus update.
        for host in holder.virus_holder:
            host.update(holder)

        for host in holder.virus_holder:

            if host not in holder.stats.dead_viruses and host.dead:
                holder.stats.dead_viruses.append(host)

            if host.dead and host.death_scene_time <= 0:
                holder.virus_holder.pop(holder.virus_holder.index(host))

        for host in holder.virus_holder:
            host.draw(screen, holder)

        # Hearts update
        for host in holder.hearts_holder:
            host.update(holder)

        for host in holder.hearts_holder:
            if not host.full:
                holder.hearts_holder.pop(holder.hearts_holder.index(host))

        for host in holder.hearts_holder:
            host.draw(screen, holder)

        # Potions update
        for host in holder.potion_holder:
            host.update(holder)

        for host in holder.potion_holder:
            if not host.full:
                holder.potion_holder.pop(holder.potion_holder.index(host))

        for host in holder.potion_holder:
            host.draw(screen, holder)

        holder.unicorn.update(screen, holder)
        holder.unicorn.draw(screen, holder)
        holder.stats.update(screen, holder, background)
        pygame.display.update(holder.dirtyrects)
        holder.reset_dirtyrects()
        clock.tick(50)


if __name__ == "__main__":
    main()
    # make this a function of the StatsBar and place it inside main.
    print(
        f"""
    + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + 

    Game stats (*_*)

    + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + 

    Total time lasted        => {holder.stats.final_points}
    Total viruses eliminated => {len(holder.stats.dead_viruses)}

    + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + 
    """
    )
