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

import pygame
from pygame.locals import *

from utils import load_image

from basemodel import BaseModel


class Unicorn(BaseModel):
    """
    Main player class
    
    boundary_check; checks for boundaries
    """

    check = {"limite": (480 - 40), "reset": (473 - 40)}

    def boundary_check(self):
        """Check the boundaries of the rect."""
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y < 34:
            self.rect.y = 35

        if self.rect.x > self.check["limite"]:
            self.rect.x = self.check["reset"]
        if self.rect.y > self.check["limite"]:
            self.rect.y = self.check["reset"]

    def activate_shield(self, screen):
        """Activate the unicorn shield"""
        shield = pygame.Surface(self.image.get_size())
        shield.fill((102, 255, 102))
        screen.blit(shield, (self.rect.x, self.rect.y))

    def state(self, key, screen):
        """Capture actions for the unicorn """
        self.shield = False
        self.rotate = False

        if key[K_ESCAPE]:
            exit(1)

        if key[K_DOWN]:
            self.rect = self.rect.move(0, 15)
            print("[*] abajo")

        if key[K_UP]:
            self.rect = self.rect.move(0, -15)
            print("[*] arriba")

        if key[K_RIGHT]:
            self.image = load_image("unicorn.png")
            copy_pos = (self.rect.x, self.rect.y)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = copy_pos
            self.rect = self.rect.move(15, 0)
            print("[*] derecha")

        if key[K_LEFT]:
            self.image = load_image("left_unicorn.png")
            copy_pos = (self.rect.x, self.rect.y)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = copy_pos
            self.rect = self.rect.move(-15, 0)
            print("[*] izquierda")

        if key[K_SPACE]:
            self.shield = True
            print("[*] escudo protector activado")

        if key[K_r]:
            self.rotate = True
            print("[*] rotate")

        self.boundary_check()

    def draw(self, screen):
        if self.rotate:
            self.image = pygame.transform.rotate(self.image, 90)

        if self.shield:
            self.activate_shield(screen)
        screen.blit(self.image, self.rect)
