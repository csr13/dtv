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

import pygame

from config import SCREENRECT
from utils.basemodel import BaseModel


class Potion(BaseModel):
    def __init__(self, img, **kwargs):
        super().__init__(img, **kwargs)
        self.full = True
        self.rect.x = 0
        self.rect.y = random.randint(1, 420)
        self.facing = random.choice((-1, 1)) * 10
        self.rect.right = SCREENRECT.right
        self.effect = 50

    def consume(self, taker):
        """Consume method, gives energy to the taker"""

        if hasattr(taker, "shield_energy"):
            if taker.shield_energy < 250:
                taker.shield_energy += (
                    (250 - taker.shield_energy)
                    if (200 <= taker.shield_energy <= 250)
                    else self.effect
                )
            elif taker.shield_energy == 250:
                pass

    @classmethod
    def replicate(potion, rate, holder):
        """Replicate a potion given a few data"""

        if rate < 60:
            spawn = 100
        elif 60 < rate < 120:
            spawn = 80
        elif 120 < rate < 180:
            spawn = 60
        else:
            spawn = 60
        if not int(random.random() * spawn):
            holder.potion_holder.append(Potion("potion.gif"))

    def update(self, holder):
        """Update the sprite on the screen"""

        self.rect.y -= 80 if self.rect.y < 80 else 0
        self.rect.x = self.rect[0] + self.facing

        images = [self.image, pygame.transform.flip(self.image, 1, 0)]
        self.image = images[random.randint(1, 6) // 3 % 2]
        self.image = pygame.transform.rotate(self.image, 360)

        if not SCREENRECT.contains(self.rect):
            holder_index = holder.potion_holder.index(self.rect)
            holder.potion_holder.pop(holder_index)
            self.facing = -self.facing
