# Copyright 2020 C. Sanchez Roman
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import random

import pygame
from pygame.locals import *
from config import SCREENRECT
from utils import load_image
from basemodel import BaseModel


class Virus(BaseModel):
    """
    <Inf3kt Th3 C0n$trUct$>
    """

    def __init__(self, img, **kwargs):
        super().__init__(img, **kwargs)
        self.dead = bool(0)
        self.rect[0] = 0
        self.rect[1] = random.randint(1, 420)
        self.facing = random.choice((-1, 1,)) * 10
        self.rect.right = SCREENRECT.right
        self.death_scene_time = 30

    @classmethod
    def replicate(host, rate, holder):
        """
        <R3pliC@t3 S3lf> - difficulty level
        """

        # Increment the replication rate each minute of gameplay
        # for three minutes, after that set the difficulty to legendary

        if rate < 60:
            difficulty = 19  # rookie
        elif 60 < rate < 120:
            difficulty = 10  # medium
        elif 120 < rate < 180:
            difficulty = 7  # very hard
        else:
            difficulty = 3  # legendary

        if not int(random.random() * difficulty):
            # Check to see if the player is not just
            # standing in the corners

            holder.virus_holder.append(Virus("virus.gif"))

    def death_scene(self):
        """
        <Dr@m@tiK Sc3Ne>
        """

        position = self.get_current_position()
        self.image = load_image("x_x.gif")
        self.rect = self.image.get_rect()
        self.rect[0], self.rect[1] = position

    def update(self, holder):
        """
        <Mut@t3>.
        """

        holder_index = holder.virus_holder.index(self.rect)

        if self.rect.y < 50:
            self.rect[1] -= 80

        if self.dead:
            self.death_scene_time -= 1

            # This is so that when the player hits the enemies
            # their guts just 'bounce' off.

            if not hasattr(self, "impact"):
                self.impact = random.choice(["up", "down"])

            if self.impact == "down":
                self.rect[1], self.rect[0] = (
                    (self.rect[1] + 6),
                    (self.rect[0] + 10),
                )
            else:
                self.rect[1], self.rect[0] = (
                    (self.rect[1] - 6),
                    (self.rect[0] + 10),
                )

        self.rect[0] = self.rect[0] + self.facing

        if not SCREENRECT.contains(self.rect):
            holder.virus_holder.pop(holder_index)
            self.facing = -self.facing
