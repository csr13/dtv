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

from config import CHECK, SCREENRECT
from utils import load_image

from basemodel import BaseModel


class Virus(BaseModel):
    """<Inf3kt Th3 C0n$trUct$>"""

    def __init__(self, img, **kwargs):
        super().__init__(img, **kwargs)
        self.facing = random.randint(-1, 1) * random.randint(10, 13)
        if self.facing < 0:
            self.rect.right = SCREENRECT.right

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        global SCREENRECT
        self.rect[0] = self.rect[0] + self.facing
        if not SCREENRECT.contains(self.rect):
            self.facing = -self.facing
            self.rect.top = self.rect.bottom + 3
            self.rect = self.rect.clamp(SCREENRECT)
