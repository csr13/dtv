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
    """

    def __init__(self, img, **kwargs):
        super().__init__(img, **kwargs)
        self.dead = False
        self.alive = True

        self.shield = False
        self.shield_energy = 250

        self.dead_time = 6
        self.check = {"limite": (450 - 30), "reset": (480 - 50)}

    def boundary_check(self):
        """
        Check the boundaries of the rect.
        """
        if self.rect.x < 0:
            self.rect.x = 10
        if self.rect.y < 34:
            self.rect.y = 45

        if self.rect.x > self.check["limite"]:
            self.rect.x = self.check["reset"]
        if self.rect.y > self.check["limite"]:
            self.rect.y = self.check["reset"]

    def shield_ok(self):
        if self.shield_energy <= 0:
            return False
        return True

    def regenerate_shield_energy(self):
        if self.shield_energy < 250 and self.shield == False:
            self.shield_energy += 0.05

    def activate_shield(self, screen, holder):
        """
        Activate the unicorn shield
        """
        if self.shield_ok():
            shield = pygame.Surface(self.image.get_size())
            shield.fill((102, 255, 102))
            shield_blit = screen.blit(shield, (self.rect.x, self.rect.y))
            holder.dirtyrects.append(shield_blit)
            self.shield_energy -= 1

    def state(self, key, screen):
        """
        Capture actions for the unicorn
        """

        self.shield = False
        self.rotate = False

        if key[K_ESCAPE]:
            exit(1)

        if key[K_DOWN]:
            self.rect = self.rect.move(0, 20)

        if key[K_UP]:
            self.rect = self.rect.move(0, -20)

        if key[K_RIGHT]:
            self.image = load_image("unicorn.png")
            copy_pos = (self.rect.x, self.rect.y)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = copy_pos
            self.rect = self.rect.move(15, 0)

        if key[K_LEFT]:
            self.image = load_image("left_unicorn.png")
            copy_pos = (self.rect.x, self.rect.y)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = copy_pos
            self.rect = self.rect.move(-15, 0)

        if key[K_SPACE]:
            if self.shield_energy <= 0:
                self.shield = False
            else:
                self.shield = True
            self.rotate = True
            print("[*] escudo protector activado")

        self.boundary_check()

    def death_scene(self):
        """
        Dramatic scene.
        """
        position = (self.rect[0], self.rect[1])
        self.image = load_image("x_x.gif")
        self.rect = self.image.get_rect()
        self.rect[0], self.rect[1] = position

    def update(self, screen, holder):
        """
        Update
        """
        if self.shield:
            self.activate_shield(screen, holder)

        if self.dead:
            self.dead_time -= 1

        if self.rotate:
            self.image = pygame.transform.rotate(self.image, 90)

        self.regenerate_shield_energy()
