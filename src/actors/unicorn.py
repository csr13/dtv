# Copyright 2020 C. Sanchez Roman
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
import sys

sys.path.append("..")

import pygame
from pygame.locals import *

from config import SOUNDS_PATH
from utils.basemodel import BaseModel
from utils.utils import load_image


class Unicorn(BaseModel):
    """
    Uni horned main player.
    """

    def __init__(self, img, **kwargs):
        super().__init__(img, **kwargs)
        self.alive = True
        self.life = 250
        self.dead = False
        self.dead_scene_time = 10
        self.speed = 20
        self.shield = False
        self.shield_energy = 250
        self.hit = False
        self.hit_time = 6
        self.health_ok = lambda: False if self.life <= 0 else True
        self.shield_ok = lambda: False if self.shield_energy <= 0 else True
        self.kill_sound = pygame.mixer.Sound(os.path.join(SOUNDS_PATH, "saw_sound.wav"))

    def regenerate_life(self):
        """Regenerates life"""

        self.life += 0.025 if self.life < 250 else 0

    def regenerate_shield_energy(self):
        """Regenerates shield energy"""

        self.shield_energy += (
            0.036 if self.shield_energy < 250 and self.shield == False else 0
        )

    def activate_shield(self, screen, holder):
        """Activate the unicorn shield."""

        if self.shield_ok():
            shield = pygame.Surface(self.image.get_size())
            shield.fill((0, 255, 0))
            shield_blit = screen.blit(shield, self.get_current_position())
            holder.dirtyrects.append(shield_blit)
            self.shield_energy -= 1

    def state(self, key, screen):
        """Keylogger"""

        self.shield = False
        self.rotate = False

        if key[K_SPACE]:
            if not self.shield_ok():
                self.shield = False
            elif self.shield_ok():
                self.shield = True
                self.rotate = True

        if key[K_DOWN]:
            if not self.rect.y > 369:
                self.rect = self.rect.move(0, self.speed)

        if key[K_UP]:
            if not self.rect.y < 82:
                self.rect = self.rect.move(0, -self.speed)

        if key[K_RIGHT]:
            self.image = load_image("unicorn.png")
            copy_pos = self.get_current_position()
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = copy_pos

            if not self.rect.x > 680:
                self.rect = self.rect.move(self.speed, 0)

        if key[K_LEFT]:
            self.image = load_image("left_unicorn.png")
            copy_pos = self.get_current_position()
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = copy_pos

            if not self.rect.x < 20:
                self.rect = self.rect.move(-self.speed, 0)

    def death_scene(self):
        """Dramatic scene."""

        position = self.get_current_position()
        self.image = load_image("x_x.gif")
        self.rect = self.image.get_rect()
        self.rect[0], self.rect[1] = position
        self.dead = True

    def hit_scene(self, screen, holder):

        self.image = pygame.transform.rotate(self.image, 180)
        effect = pygame.Surface(self.image.get_size())
        effect.fill((255, 0, 0))
        effect_blit = screen.blit(effect, self.get_current_position())
        holder.dirtyrects.append(effect_blit)

    def kill_enemy(self, enemy):
        """Kill an enemy and play a sound"""
        self.kill_sound.play()
        enemy.death_scene()
        enemy.dead = True

    def update(self, screen, holder):
        """Update things."""

        if self.dead:
            self.dead_scene_time -= 1

        if self.hit:
            self.life -= 20
            self.hit = False

        if self.shield:
            self.activate_shield(screen, holder)

        if self.rotate:
            self.image = pygame.transform.rotate(self.image, 90)

        self.regenerate_shield_energy()
        self.regenerate_life()
