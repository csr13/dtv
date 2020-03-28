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

import pygame
from pygame.locals import *

from config import SCREENRECT
from utils import load_image

from basemodel import BaseModel


class Virus(BaseModel):
    """<Inf3kt Th3 C0n$trUct$>"""

    def __init__(self, img, **kwargs):
        super().__init__(img, **kwargs)
        self.rect[0] = 0
        self.rect[1] = random.randint(1, 420)
        self.facing = random.choice((-1, 1,)) * 10
        self.rect.right = SCREENRECT.right
        self.dead = False
        self.death_scene_time = 30

    def get_position(self):
        """
        <G3t p0$iti0n 0f h0$t>
        """
        return (
            self.rect[0],
            self.rect[1],
        )

    def death_scene(self):
        """
        <Dr@m@tiK Sc3Ne>
        """
        position = self.get_position()
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
            self.death_scene()
            self.death_scene_time -= 1
            self.rect[1] -= 1

        self.rect[0] = self.rect[0] + self.facing

        if not SCREENRECT.contains(self.rect):
            holder.virus_holder.pop(holder_index)
            self.facing = -self.facing
