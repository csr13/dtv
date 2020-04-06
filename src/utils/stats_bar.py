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
import sys

sys.path.append("..")

import pygame
from pygame.locals import *

from config import SCREENRECT
from utils.basemodel import BaseModel
from utils.utils import load_image, writer


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

        time_text, time_position = self.writer(
            phrase="Time",
            font="ubuntumono",
            size=12,
            color=(255, 255, 51),
            where={"top": 45, "right": 360},
        )
        time_number_text, time_number_position = self.writer(
            phrase=f"{self.get_current_game_time()} ",
            font="ubuntumono",
            size=12,
            color=(255, 255, 51),
            where={"top": 45, "right": 423},
        )
        holder.dirtyrects.append(screen.blit(time_number_text, time_number_position))
        holder.dirtyrects.append(screen.blit(time_text, time_position))

    def generate_energy_bar_text(self, screen, holder):
        """
        Generates energy bar and appends a blit to be updated.
        """

        energy_text, energy_position = self.writer(
            phrase=f"Shield ",
            font="ubuntumono",
            size=12,
            color=(255, 255, 51),
            where={"top": 10, "right": 57},
        )
        holder.dirtyrects.append(screen.blit(energy_text, energy_position))

    def generate_energy_bar(self, screen, holder):
        """
        Generate the energy bar append its blit to be updated.
        """

        energy = holder.unicorn.shield_energy
        energy_bar_rect = pygame.Rect(0, 0, energy, 35)
        energy_bar_bkgd = pygame.Surface(energy_bar_rect.size)
        energy_bar_bkgd.fill((0, 255, 0))
        holder.dirtyrects.append(screen.blit(energy_bar_bkgd, (70, 0)))

    def generate_unicorn_life_text(self, screen, holder):
        """
        Generated the life text with numerical measurement.
        """

        lives_text, lives_text_position = self.writer(
            phrase=f"Energy ",
            font="ubuntumono",
            size=12,
            color=(255, 255, 255),
            where={"top": 45, "right": 57},
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
            life_bar_rect = pygame.Rect(0, 0, life, 33)
        except:
            return
        life_bar_bkgd = pygame.Surface(life_bar_rect.size)
        life_bar_bkgd.fill((0, 0, 220))
        holder.dirtyrects.append(screen.blit(life_bar_bkgd, (70, 36)))

    def generate_grid(self, background):
        """
        Generate a bottom border that contains the stats
        """
        pygame.draw.line(
            background, (0, 255, 0), (800, 70), (0, 70),
        )
        pygame.draw.line(background, (0, 255, 0), (320, 70), (320, 0))
        pygame.draw.line(background, (0, 255, 0), (800, 0), (0, 0))
        pygame.draw.line(background, (0, 255, 0), (320, 35), (0, 35))

    def generate_virus_killed(self, screen, holder):
        """
        Generate stats for viruses killed
        """
        kill_count = len(self.dead_viruses)
        kill_count_text, kill_count_text_position = self.writer(
            phrase=f"Kill count ",
            font="ubuntumono",
            size=12,
            color=(0, 255, 0),
            where={"top": 10, "right": 400},
        )
        kill_count_number, kill_count_number_position = self.writer(
            phrase=str(kill_count),
            font="ubuntumono",
            size=12,
            color=(0, 255, 0),
            where={"top": 10, "right": 416},
        )
        holder.dirtyrects.append(screen.blit(kill_count_text, kill_count_text_position))
        holder.dirtyrects.append(
            screen.blit(kill_count_number, kill_count_number_position)
        )

    def update(self, screen, holder, background=None):
        """
        Update everyting.
        """
        self.generate_unicorn_life_text(screen, holder)
        self.generate_unicorn_life_bar(screen, holder)
        self.generate_energy_bar_text(screen, holder)
        self.generate_virus_killed(screen, holder)
        self.generate_energy_bar(screen, holder)
        self.generate_game_time(screen, holder)
        self.generate_grid(background)
