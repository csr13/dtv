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


class StatsBar:
    """
    Stats Bar class
    """

    def __init__(self):
        self.energy = 0
        self.lives = 0
        self.points = {"time_points_start": time.time(), "time_points_end": None}
        self.writer = writer

    def get_current_points(self):
        """
        This is ugly but otherwise if we increase complexity it might 'leak' 
        out points from the player x_x
        """
        return divmod(
            (math.ceil(time.time()) - self.points["times_point_start"]), 1000
        )[1]

    def generate_background(self, screen, holder):
        """
        Generate the background for the stat bar.
        """
        background_rect = pygame.Rect(0, 0, SCREENRECT.width, 50)
        background = pygame.Surface(background_rect.size)
        background.fill((0, 0, 0))
        pygame.draw.line(background, (120, 0, 0), (800, 49), (0, 49))
        pygame.draw.line(background, (120, 0, 0), (800, 0), (0, 0))
        pygame.draw.line(background, (120, 0, 0), (799, 49), (799, 0))
        pygame.draw.line(background, (120, 0, 0), (0, 49), (0, 0))
        holder.dirtyrects.append(screen.blit(background, (0, 0)))

    def generate_energy_bar(self, screen, energy, holder):
        """
        Generate the energy bar
        """
        # generate text

        energy_text, energy_position = self.writer(
            phrase=f"energy >> {math.ceil(energy)} ",
            font="ubuntumono",
            size=12,
            color=(255, 255, 51),
            where={"top": 15, "right": 98},
        )
        # generate bar
        width = energy
        energy_bar_rect = pygame.Rect(0, 0, energy, 15)
        energy_bar_bkgd = pygame.Surface(energy_bar_rect.size)
        energy_bar_bkgd.fill((0, 255, 0))

        holder.dirtyrects.append(screen.blit(energy_text, energy_position))
        holder.dirtyrects.append(screen.blit(energy_bar_bkgd, (100, 15)))

    def get_final_points(self):
        final_points = self.get_current_points()
        return f"Final score :: {final_points}"

    def generate(self, screen, energy, holder):
        self.generate_background(screen, holder)
        self.generate_energy_bar(screen, energy, holder)

    def update(self, shield_energy, lives=None):
        """
        We should update the width of the rect bar that represents the shields energy
        We should create a couple of properties 
        """
        pass
