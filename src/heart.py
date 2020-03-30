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
import math

import random
import pygame
from pygame.locals import *
from config import SCREENRECT
from utils import load_image
from basemodel import BaseModel


class Heart(BaseModel):
    def __init__(self, img, **kwargs):
        super().__init__(img, **kwargs)
        self.rect[0] = 0
        self.rect[1] = random.randint(1, 420)
        self.facing = random.choice((-1, 1)) * 10
        self.rect.right = SCREENRECT.right
        self.vanish_time = 30
        self.full = True
        self.effect = 69

    def consume(self, taker):
        """
        Consume life and give it to the taker.
        """

        if hasattr(taker, "life"):
            if taker.life == 250:
                pass
            elif 181 <= taker.life < 250:
                taker.life += 250 - taker.life
            else:
                taker.life += self.effect

            self.full = False

    @classmethod
    def replicate(heart, rate, holder):
        """
        Spawn random energy.
        """

        if rate < 60:
            refresh = 200
        elif 60 < rate < 120:
            refresh = 150
        elif 120 < rate < 180:
            refresh = 125
        else:
            refresh = 100

        if not int(random.random() * refresh):
            holder.hearts_holder.append(Heart("heart.png"))

    def update(self, holder):
        """
        Update before drawing
        """
        holder_index = holder.hearts_holder.index(self.rect)
        if self.rect.y < 50:
            self.rect[1] -= 80

        if not self.full:
            self.vanish_time -= 1
            self.rect[1], self.rect[0] = (
                (self.rect[1] + 6),
                (self.rect[0] + 10),
            )

        self.rect[0] = self.rect[0] + self.facing

        if not SCREENRECT.contains(self.rect):
            holder.hearts_holder.pop(holder_index)
            self.facing = -self.facing
