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
import math
import time

import pygame
from pygame.locals import *

from utils import load_image

from basemodel import BaseModel
from config import SCREENRECT
from utils import writer


class StatsBar(object):
    """
    Stats Bar class
    """

    def __init__(self):
        self.game_start = time.time()
        self.writer = writer
        self.dead_viruses = []

    def get_current_game_time(self):
        """
        This is ugly but otherwise if we increase complexity it might 'leak' 
        out miliseconds from game time.
        """

        return math.ceil(divmod((math.ceil(time.time()) - self.game_start), 1000)[1])

    def generate_game_time(self, screen, holder):
        """
        Generates points and appends a blit to be updated.
        """

        points_text, points_position = self.writer(
            phrase=f"{self.get_current_game_time()} ",
            font="ubuntumono",
            size=12,
            color=(255, 255, 51),
            where={"top": 17, "right": 780},
        )
        holder.dirtyrects.append(screen.blit(points_text, points_position))

    def generate_energy_bar_text(self, screen, holder):
        """
        Generates energy bar and appends a blit to be updated.
        """

        energy_text, energy_position = self.writer(
            phrase=f"Shield {math.ceil(holder.unicorn.shield_energy)} ",
            font="ubuntumono",
            size=12,
            color=(255, 255, 51),
            where={"top": 16, "right": 98},
        )
        holder.dirtyrects.append(screen.blit(energy_text, energy_position))

    def generate_energy_bar(self, screen, holder):
        """
        Generate the energy bar append its blit to be updated.
        """

        energy = holder.unicorn.shield_energy
        energy_bar_rect = pygame.Rect(0, 0, energy, 15)
        energy_bar_bkgd = pygame.Surface(energy_bar_rect.size)
        energy_bar_bkgd.fill((0, 255, 0))
        holder.dirtyrects.append(screen.blit(energy_bar_bkgd, (100, 15)))

    def generate_unicorn_life_text(self, screen, holder):
        """
        Generated the life text with numerical measurement.
        """

        lives_text, lives_text_position = self.writer(
            phrase=f"Energy {math.ceil(holder.unicorn.life)}",
            font="ubuntumono",
            size=12,
            color=(255, 255, 255),
            where={"top": 33, "right": 98},
        )
        holder.dirtyrects.append(screen.blit(lives_text, lives_text_position))

    def generate_unicorn_life_bar(self, screen, holder):
        """
        Generate the unicorns life bar.
        """
        life = math.ceil(holder.unicorn.life)
        if life < 1:
            life = 1
        try:
            life_bar_rect = pygame.Rect(0, 0, life, 15)
        except:
            return
        life_bar_bkgd = pygame.Surface(life_bar_rect.size)
        life_bar_bkgd.fill((0, 0, 220))
        holder.dirtyrects.append(screen.blit(life_bar_bkgd, (100, 35)))

    def update(self, screen, holder):
        """
        Update everyting.
        """

        self.generate_unicorn_life_text(screen, holder)
        self.generate_unicorn_life_bar(screen, holder)
        self.generate_energy_bar_text(screen, holder)
        self.generate_energy_bar(screen, holder)
        self.generate_game_time(screen, holder)
