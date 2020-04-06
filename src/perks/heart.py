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
import sys

sys.path.append("..")

import pdb

import pygame

from config import SCREENRECT
from utils.basemodel import BaseModel


class Heart(BaseModel):
    """
    Heart object representation of a gameplay heart.
    ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    If the heart is consumed it inscreases the players life by 50
    life points.

    ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    """

    def __init__(self, img, **kwargs):
        super().__init__(img, **kwargs)
        self.full = True
        self.rect[0] = 0
        self.rect[1] = random.randint(1, 420)
        self.facing = random.choice((-1, 1)) * 10
        self.rect.right = SCREENRECT.right
        self.effect = 50

    def consume(self, taker):
        """Consume life and give it to the taker."""

        if hasattr(taker, "life"):
            if taker.life < 250:
                if 181 <= taker.life <= 250:
                    taker.life += 250 - taker.life
                else:
                    taker.life += self.effect
            elif taker.life == 250:
                pass

    @classmethod
    def replicate(heart, rate, holder):
        """Spawn random energy."""

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

    def consumed_scene(self, *args):
        """This scene lasts for as long as vanishing_time is > 0"""

        holder = args[2]
        screen = args[0]
        player = holder.unicorn

        def glow():
            """Trigger an effect when the heart is consumed"""

            effect = pygame.Surface(player.image.get_size())
            effect.fill((0, 0, 255))
            effect_blit = screen.blit(effect, player.get_current_position())
            holder.dirtyrects.append(effect_blit)

        self.consume(player)
        glow()

    def update(self, holder):
        """Update before drawing"""

        self.rect[1] -= 80 if self.rect.y < 80 else 0
        self.rect[0] = self.rect[0] + self.facing

        if not SCREENRECT.contains(self.rect):
            holder_index = holder.hearts_holder.index(self.rect)
            holder.hearts_holder.pop(holder_index)
            self.facing = -self.facing
